
import re

def _terms(text):
    return set(re.findall(r"[a-zA-Z][a-zA-Z0-9+#./-]{2,}", (text or "").lower()))

def calculate_score(parsed, job_description=""):
    personal=parsed.get("personal_information",{})
    skills=parsed.get("skills_flat") or [
        item for values in (parsed.get("skills") or {}).values() for item in values
    ]
    categories={
        "Contact details": 15 if personal.get("email") and personal.get("phone") else 8 if personal.get("email") or personal.get("phone") else 0,
        "Skills relevance": min(20, round(len(skills)*1.5)),
        "Work experience": 20 if parsed.get("experience_records") or parsed.get("experience") else 0,
        "Projects": 15 if parsed.get("project_records") or parsed.get("projects") else 0,
        "Education": 10 if parsed.get("education") else 0,
        "Certifications": 5 if parsed.get("certifications") else 2,
        "Professional links": 5 if any(personal.get(k) for k in ("linkedin","github","portfolio")) else 0,
    }
    job_match=5
    if job_description and job_description.strip():
        jd_terms=_terms(job_description)
        stop={"the","and","with","for","you","are","will","our","this","that","from","have","has","your","work","role","job","years","year","ability","strong","experience","skills","knowledge"}
        jd_terms={t for t in jd_terms if t not in stop}
        resume_terms=_terms(" ".join(skills)+" "+" ".join(parsed.get("experience",[]))+" "+" ".join(parsed.get("projects",[])))
        job_match=round(10*len(jd_terms & resume_terms)/max(1,min(15,len(jd_terms))))
    categories["Job description match"]=job_match
    total=min(100,max(0,sum(categories.values())))
    rating="Excellent" if total>=85 else "Strong" if total>=70 else "Developing" if total>=50 else "Needs improvement"
    # The score is intentionally transparent and heuristic.
    return {
        "total":total,
        "overall_score":total,
        "rating":rating,
        "breakdown":categories,
        "category_scores":categories,
        "summary":f"Resume structure and content signals currently indicate {rating.lower()} ATS readiness. Review the category breakdown and validate all extracted details."
    }

def score_label(score):
    if isinstance(score,dict):
        score=score.get("total",score.get("overall_score",0))
    try: score=float(score)
    except (TypeError,ValueError): score=0
    if score>=85: return "Excellent"
    if score>=70: return "Strong"
    if score>=50: return "Developing"
    return "Needs improvement"
