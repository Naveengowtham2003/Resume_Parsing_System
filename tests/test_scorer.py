
from modules.resume_scorer import calculate_score, score_label

def test_score_is_bounded_and_has_legacy_fields():
    result=calculate_score({"personal_information":{},"skills":{},"skills_flat":[],"skill_count":0,"experience_records":[],"experience":[],"project_records":[],"projects":[],"education":[],"certifications":[]})
    assert 0 <= result["total"] <= 100
    assert result["total"] == result["overall_score"]
    assert "breakdown" in result
    assert score_label(result["total"])

def test_fuller_profile_scores_higher():
    empty={"personal_information":{},"skills":{},"skills_flat":[],"skill_count":0,"experience_records":[],"experience":[],"project_records":[],"projects":[],"education":[],"certifications":[]}
    filled={"personal_information":{"email":"a@b.com","phone":"1234567890","linkedin":"https://linkedin.com/in/a"},"skills":{"Programming":["Python","SQL"]},"skills_flat":["Python","SQL"],"skill_count":2,"experience_records":[{}],"experience":["Python Developer"],"project_records":[{}],"projects":["Project"],"education":["B.E."],"certifications":["AWS"]}
    assert calculate_score(filled)["total"] > calculate_score(empty)["total"]
