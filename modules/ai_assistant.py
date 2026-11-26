"""Ollama integration for ResumeIQ.

Uses the local Ollama HTTP API. Configure with:
    OLLAMA_BASE_URL=http://127.0.0.1:11434
    OLLAMA_MODEL=llama3.2
    OLLAMA_TIMEOUT=600
"""

import json
import os
import socket
import urllib.error
import urllib.request


def _base_url():
    value = (
        os.getenv("OLLAMA_BASE_URL")
        or os.getenv("OLLAMA_HOST")
        or "http://127.0.0.1:11434"
    ).strip().rstrip("/")

    if not value.startswith(("http://", "https://")):
        value = "http://" + value

    return value


def _read_json(url, timeout, payload=None):
    data = None
    headers = {"Accept": "application/json"}

    if payload is not None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"

    request = urllib.request.Request(url, data=data, headers=headers)

    with urllib.request.urlopen(request, timeout=timeout) as response:
        raw = response.read().decode("utf-8", errors="replace")
        return json.loads(raw) if raw.strip() else {}


def _connection_error_message(base_url, exc):
    return (
        "### Ollama is not reachable\n\n"
        f"ResumeIQ could not connect to `{base_url}`.\n\n"
        "1. Open the Ollama application from the Windows Start menu.\n"
        "2. In a separate PowerShell window, run `ollama serve` if the service "
        "is not already running.\n"
        "3. Verify the API with "
        "`Invoke-RestMethod http://127.0.0.1:11434/api/tags`.\n\n"
        f"Technical detail: `{exc}`"
    )


def generate_ai_review(parsed, score, job_description=""):
    """Generate a grounded resume review using the local Ollama service.

    Returns a Markdown string. Connection/model/time-out problems are returned
    as actionable Markdown messages so the Streamlit page can display them.
    """
    base_url = _base_url()
    model = os.getenv("OLLAMA_MODEL", "llama3.2").strip() or "llama3.2"

    try:
        connection_timeout = float(os.getenv("OLLAMA_CONNECT_TIMEOUT", "8"))
        generation_timeout = float(os.getenv("OLLAMA_TIMEOUT", "600"))
    except ValueError:
        connection_timeout, generation_timeout = 8.0, 600.0

    # Check the service before attempting a potentially long model generation.
    try:
        tags_data = _read_json(
            f"{base_url}/api/tags",
            timeout=connection_timeout
        )
    except (urllib.error.URLError, TimeoutError, socket.timeout, OSError) as exc:
        return _connection_error_message(base_url, exc)
    except Exception as exc:
        return (
            "### Could not check the Ollama service\n\n"
            f"Endpoint: `{base_url}/api/tags`\n\nTechnical detail: `{exc}`"
        )

    installed_models = [
        item.get("name", "")
        for item in tags_data.get("models", [])
        if isinstance(item, dict)
    ]
    model_is_installed = any(
        name == model or name.startswith(model + ":")
        for name in installed_models
    )

    if not model_is_installed:
        installed_text = ", ".join(installed_models) if installed_models else "No models found"
        return (
            f"### Model `{model}` is not installed in Ollama\n\n"
            "Run this in PowerShell:\n\n"
            f"```powershell\nollama pull {model}\n```\n\n"
            f"Models currently available: `{installed_text}`"
        )

    score_value = score.get("overall_score", score.get("total", "Not available"))
    parsed_json = json.dumps(parsed, ensure_ascii=False, default=str)
    prompt = f"""You are ResumeIQ, a careful and practical resume reviewer.

Review only the information present in the parsed resume. Do not invent employers,
skills, qualifications, metrics, achievements, or dates. Where extraction may be
incomplete, explicitly say so. Keep advice concrete and prioritize changes.

Return these sections:
1. Overall assessment
2. Strengths supported by the resume
3. Important gaps or unclear information
4. Prioritized improvements (highest impact first)
5. Target job alignment

ATS readiness score: {score_value}/100

Parsed resume JSON:
{parsed_json[:14000]}

Target job description:
{job_description[:6000] if job_description else "Not provided"}
"""

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "keep_alive": "10m",
        "options": {
            "temperature": 0.2,
            "num_ctx": 4096
        }
    }

    try:
        result = _read_json(
            f"{base_url}/api/generate",
            timeout=generation_timeout,
            payload=payload
        )
        review = result.get("response", "").strip()
        if not review:
            return (
                "### Ollama returned an empty review\n\n"
                "Try running `ollama run " + model + "` in PowerShell to confirm "
                "the model loads, then retry AI Review."
            )
        return review

    except (TimeoutError, socket.timeout) as exc:
        return (
            "### The AI review timed out\n\n"
            "Ollama is responding, but the model did not finish generating "
            f"within {int(generation_timeout)} seconds. The first run may take "
            "longer while the model loads. Retry once, or set a longer timeout.\n\n"
            "In PowerShell, set a 15-minute timeout for the current session:\n\n"
            "```powershell\n$env:OLLAMA_TIMEOUT='900'\n```\n\n"
            f"Technical detail: `{exc}`"
        )
    except urllib.error.HTTPError as exc:
        try:
            detail = exc.read().decode("utf-8", errors="replace")[:1500]
        except Exception:
            detail = str(exc)
        return (
            "### Ollama returned an API error\n\n"
            f"HTTP status: `{exc.code}`\n\n"
            f"```text\n{detail}\n```"
        )
    except urllib.error.URLError as exc:
        return _connection_error_message(base_url, exc)
    except Exception as exc:
        return (
            "### AI review failed\n\n"
            f"Technical detail: `{type(exc).__name__}: {exc}`"
        )
