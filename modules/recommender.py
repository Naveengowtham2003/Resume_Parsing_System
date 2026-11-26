
def generate_recommendations(parsed, score, job_description=""):
    recs=[]
    info=parsed.get("personal_information",{})
    skill_count=parsed.get("skill_count",0)
    if not info.get("email") or not info.get("phone"):
        recs.append({"title":"Complete your contact information","detail":"Ensure a professional email address and reachable phone number are visible near the top of the resume.","priority":"High"})
    if not info.get("linkedin"):
        recs.append({"title":"Add a professional LinkedIn profile","detail":"Include a clean LinkedIn URL so reviewers can validate your professional background and discover relevant work.","priority":"Medium"})
    if not parsed.get("experience_records"):
        recs.append({"title":"Make employment history easy to scan","detail":"Use a standard heading and show each role with employer, job title, dates, and concise achievement-focused bullets.","priority":"High"})
    if not parsed.get("project_records"):
        recs.append({"title":"Showcase relevant projects","detail":"Add two or three projects with the problem, your contribution, technologies used, and an outcome you can substantiate.","priority":"High"})
    if skill_count<8:
        recs.append({"title":"Review the skills inventory","detail":"Include relevant tools and technologies you can confidently discuss. Group them by programming, frameworks, data, cloud and platforms.","priority":"Medium"})
    if not parsed.get("education"):
        recs.append({"title":"Add your education details","detail":"Include qualification, institution, graduation year and relevant academic details.","priority":"High"})
    if not parsed.get("certifications"):
        recs.append({"title":"Include relevant credentials where applicable","detail":"List completed, role-relevant certifications. Do not present unfinished courses as completed credentials.","priority":"Low"})
    if job_description.strip():
        recs.append({"title":"Tailor the resume to the target role","detail":"Compare the job description with your real skills and experience. Add missing keywords only when they accurately describe your background.","priority":"High"})
    if not recs:
        recs.append({"title":"Strengthen achievement statements","detail":"Use action verbs and include scope, tools and measurable outcomes wherever you can support the claim.","priority":"Medium"})
    return recs
