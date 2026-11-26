
def build_analytics(parsed, score):
    section_counts={
        "Skills":parsed.get("skill_count",0),
        "Experience":len(parsed.get("experience_records",[])),
        "Projects":len(parsed.get("project_records",[])),
        "Education":len(parsed.get("education",[])),
        "Certifications":len(parsed.get("certifications",[])),
    }
    content_metrics={
        "Skills":parsed.get("skill_count",0),
        "Experience entries":len(parsed.get("experience_records",[])),
        "Projects":len(parsed.get("project_records",[])),
        "Education entries":len(parsed.get("education",[])),
        "Certifications":len(parsed.get("certifications",[])),
    }
    return {
        "section_counts":section_counts,
        "content_metrics":content_metrics,
        "word_count":parsed.get("word_count",0),
        "detected_sections":sum(parsed.get("section_presence",{}).values()),
    }
