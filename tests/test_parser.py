
from modules.information_parser import parse_resume, calculate_extraction_confidence

def test_basic_parse_and_legacy_schema():
    text="""ALEX MORGAN
alex@example.com
+1 555 555 5555
SKILLS
Python, SQL, FastAPI
PROFESSIONAL EXPERIENCE
Acme Inc | Python Developer | 01/2023 - Present
Built data services using Python and FastAPI.
PROJECTS
Inventory Forecasting Platform
EDUCATION
B.E. Computer Science
"""
    result=parse_resume(text)
    assert result["personal_information"]["email"]=="alex@example.com"
    assert result["skill_count"] >= 2
    assert any("Python" in skills for skills in result["skills"].values())
    assert len(result["experience"]) == 1
    assert len(result["experience_records"]) == 1
    assert result["experience_records"][0]["duration"] == "01/2023 - Present"
    assert len(result["projects"]) == 1
    assert "education" in result
    assert calculate_extraction_confidence(result)>=50

def test_legacy_call_signature():
    parsed=parse_resume("JANE DOE\njane@example.com\nSKILLS\nPython", "resume.docx", embedded_links=["https://linkedin.com/in/jane"])
    assert parsed["personal_information"]["linkedin"]=="https://linkedin.com/in/jane"


def test_project_technology_line_and_date_range():
    text="""NAVEEN GOWTHAM K T
naveen@example.com
PROFESSIONAL EXPERIENCE
Capgemini | Analyst – SAP ABAP 04/2025 – Present | Bengaluru, India
Supported enterprise application development.
PROJECTS
AI-Powered Network Monitoring & Troubleshooting Agent:
Python, FastAPI, Streamlit, Isolation Forest, Hugging Face
Built a network monitoring prototype.
EDUCATION
B.E. Computer Science
"""
    parsed=parse_resume(text)
    record=parsed["experience_records"][0]
    assert record["company"]=="Capgemini"
    assert "SAP ABAP" in record["role"]
    assert record["duration"]=="04/2025 – Present"
    assert "FastAPI" in parsed["project_records"][0]["technologies"]
