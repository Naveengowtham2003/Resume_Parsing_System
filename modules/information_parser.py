
import re
from collections import OrderedDict

SKILL_CATEGORIES = OrderedDict({
    "Programming": ["python","java","javascript","typescript","c","c++","c#","sql","sap abap"],
    "AI / Machine Learning": ["machine learning","deep learning","generative ai","genai","llm","rag","nlp","tensorflow","pytorch","scikit-learn","xgboost","lightgbm","catboost","hugging face","transformers","langchain","prompt engineering","computer vision","opencv"],
    "Data & Analytics": ["pandas","numpy","matplotlib","plotly","power bi","tableau","excel","data analysis","data engineering","pyspark","spark","databricks","etl","airflow","kafka","hadoop"],
    "Backend & Web": ["fastapi","flask","django","streamlit","react","node.js","html","css","rest api","api development"],
    "Cloud & DevOps": ["aws","azure","gcp","google cloud","docker","kubernetes","git","github","ci/cd","linux"],
    "Databases": ["mysql","postgresql","mongodb","sqlite","oracle","redis"],
})

SECTION_ALIASES = {
    "experience": {"experience","work experience","professional experience","employment history","career history","internship","internships"},
    "projects": {"projects","project experience","academic projects","personal projects","key projects","project work"},
    "education": {"education","academic background","qualifications","qualification","academic details"},
    "certifications": {"certifications","certificates","licenses","courses","training"},
    "skills": {"skills","technical skills","core competencies","technical expertise","key skills"},
}

def _normalise_heading(line):
    return re.sub(r"[^a-z ]", "", line.lower()).strip()

def _clean_lines(text):
    text = (text or "").replace("\r", "\n").replace("\xa0", " ")
    out=[]
    for raw in text.splitlines():
        line=re.sub(r"\s+", " ", raw).strip()
        line=line.strip("•▪●◦\t ")
        if line:
            out.append(line)
    return out

def _split_sections(lines):
    sections={"other":[]}
    current="other"
    lookup={alias:key for key, aliases in SECTION_ALIASES.items() for alias in aliases}
    for line in lines:
        key=lookup.get(_normalise_heading(line))
        if key:
            current=key
            sections.setdefault(current,[])
            continue
        # Handle simple inline headings such as "Skills: Python, SQL"
        match=re.match(r"^([A-Za-z /&-]{3,28}):\s*(.+)$", line)
        if match:
            possible=lookup.get(_normalise_heading(match.group(1)))
            if possible:
                current=possible
                sections.setdefault(current,[]).append(match.group(2).strip())
                continue
        sections.setdefault(current,[]).append(line)
    return sections

def _extract_links(text, links):
    candidates=[]
    if isinstance(links, str):
        candidates.append(links)
    elif links:
        candidates.extend([x for x in links if isinstance(x,str)])
    candidates.extend(re.findall(r"https?://[^\s<>()]+", text or "", re.I))
    clean=[]
    for url in candidates:
        url=url.rstrip(".,;)")
        if url not in clean: clean.append(url)
    linkedin=next((u for u in clean if "linkedin.com" in u.lower()),None)
    github=next((u for u in clean if "github.com" in u.lower()),None)
    portfolio=next((u for u in clean if "linkedin.com" not in u.lower() and "github.com" not in u.lower()),None)
    return linkedin,github,portfolio,clean

def _find_skills(text):
    low=(text or "").lower()
    grouped=OrderedDict()
    for category, terms in SKILL_CATEGORIES.items():
        found=[]
        for term in terms:
            pattern=r"(?<![a-z0-9])"+re.escape(term)+r"(?![a-z0-9])"
            if re.search(pattern,low):
                display=term.upper() if term in {"sql","nlp","aws","azure","gcp","llm","rag","etl","api","ci/cd"} else term.title()
                found.append(display)
        if found: grouped[category]=found
    return grouped

_DATE_RE=re.compile(
    r"(?:\b(?:0?[1-9]|1[0-2])[/.-]\d{4}\b|\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s+\d{4}\b|\b20\d{2}\b)"
    r".{0,45}?(?:present|current|20\d{2}|ongoing)",
    re.I
)

def _parse_experience(lines):
    if not lines: return []
    # Group a role heading and its following bullets. Also supports a compact one-line entry.
    groups=[]
    current=None
    for line in lines:
        looks_heading = bool(_DATE_RE.search(line)) or ("|" in line and len(line.split()) < 22)
        if looks_heading:
            if current: groups.append(current)
            current={"heading":line,"details":[]}
        elif current is None:
            current={"heading":line,"details":[]}
        else:
            current["details"].append(line)
    if current: groups.append(current)
    records=[]
    for group in groups:
        heading=group["heading"]
        pieces=[p.strip() for p in re.split(r"\s+\|\s+",heading) if p.strip()]
        company=pieces[0] if len(pieces)>1 else ""
        role=pieces[1] if len(pieces)>1 else heading
        duration_match=_DATE_RE.search(heading)
        duration=duration_match.group(0).strip() if duration_match else ""
        # Remove dates and trailing location from the role label when possible.
        role= re.sub(r"\s+"+re.escape(duration)+r".*$", "", role, flags=re.I).strip() if duration else role
        records.append({
            "company":company,
            "role":role,
            "duration":duration,
            "header":heading,
            "description":" ".join(group["details"]),
            "bullets":group["details"]
        })
    return records

def _parse_projects(lines):
    if not lines: return []
    records=[]
    current=None
    tech_re=re.compile(r"^(?:tech(?:nologies)?(?:\s*stack)?|tools)\s*:\s*(.+)$",re.I)
    for line in lines:
        tech=tech_re.match(line)
        is_heading = (
            len(line.split()) <= 16 and
            (line.endswith(":") or re.match(r"^(?:[A-Z][\w/&()+-]+(?:\s+[A-Z][\w/&()+-]+){0,12})$",line) is not None)
        )
        looks_like_stack = (
            current is not None and "," in line and len(line.split()) <= 18
            and not line.endswith((".", "!", "?"))
        )
        if tech and current:
            current["technologies"] += [x.strip() for x in re.split(r"[,|]",tech.group(1)) if x.strip()]
        elif is_heading:
            if current: records.append(current)
            current={"name":line.rstrip(":."),"technologies":[],"description":"","bullets":[]}
        elif looks_like_stack:
            current["technologies"] += [x.strip() for x in re.split(r"[,|]",line) if x.strip()]
        elif current:
            current["bullets"].append(line)
            current["description"] += (" " if current["description"] else "")+line
    if current: records.append(current)
    if not records and lines:
        records=[{"name":"Projects","technologies":[],"description":" ".join(lines),"bullets":lines}]
    return records

def parse_resume(text, filename=None, embedded_links=None, links=None):
    """Parse resume text. Accepts both the current and legacy app call signatures."""
    all_links=list(links or [])
    if embedded_links:
        all_links.extend(embedded_links if isinstance(embedded_links,(list,tuple)) else [embedded_links])
    if isinstance(filename,str) and filename.startswith(("http://","https://")):
        all_links.append(filename)

    lines=_clean_lines(text)
    joined="\n".join(lines)
    sections=_split_sections(lines)
    first_lines=lines[:10]
    name=next((x for x in first_lines if re.fullmatch(r"[A-Z][A-Z .'-]{3,}",x) and not any(w in x for w in ["RESUME","CURRICULUM VITAE"])),None)
    email=next(iter(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",joined)),None)
    phones=re.findall(r"(?:\+\d{1,3}[\s.-]?)?(?:\(?\d{2,5}\)?[\s.-]?)?\d{3,5}[\s.-]?\d{4,6}",joined)
    phone=next((p.strip() for p in phones if len(re.sub(r"\D","",p))>=10),None)
    linkedin,github,portfolio,all_urls=_extract_links(joined,all_links)

    skill_groups=_find_skills(joined)
    skill_flat=[skill for values in skill_groups.values() for skill in values]
    experience_records=_parse_experience(sections.get("experience",[]))
    project_records=_parse_projects(sections.get("projects",[]))
    education=sections.get("education",[])
    certifications=sections.get("certifications",[])
    # Include a conservative experience string list for older app versions.
    experience_legacy=[
        " — ".join(x for x in [r.get("role"),r.get("company"),r.get("duration"),r.get("description")] if x)
        for r in experience_records
    ]
    return {
        "personal_information":{
            "name":name,"email":email,"phone":phone,"location":None,
            "linkedin":linkedin,"github":github,"portfolio":portfolio,"other_links":all_urls
        },
        "skills":dict(skill_groups),
        "skills_flat":skill_flat,
        "skill_count":len(skill_flat),
        "experience":experience_legacy,
        "experience_records":experience_records,
        "projects":[p["name"] for p in project_records],
        "project_records":project_records,
        "education":education,
        "certifications":certifications,
        "section_presence":{k:bool(sections.get(k)) for k in SECTION_ALIASES},
        "word_count":len(joined.split()),
        "raw_line_count":len(lines),
    }

def calculate_extraction_confidence(parsed):
    personal=parsed.get("personal_information",{})
    signals=[
        bool(personal.get("name")),bool(personal.get("email")),bool(personal.get("phone")),
        bool(parsed.get("skills_flat") or parsed.get("skills")),
        bool(parsed.get("experience_records") or parsed.get("experience")),
        bool(parsed.get("project_records") or parsed.get("projects")),
        bool(parsed.get("education"))
    ]
    return round(100*sum(signals)/len(signals))
