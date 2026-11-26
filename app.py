
import json
import streamlit as st
import pandas as pd
import plotly.express as px

from modules.resume_extractor import extract_document
from modules.information_parser import parse_resume, calculate_extraction_confidence
from modules.resume_scorer import calculate_score, score_label
from modules.recommender import generate_recommendations
from modules.analytics import build_analytics
from modules.ai_assistant import generate_ai_review

st.set_page_config(
    page_title="ResumeIQ | Resume Intelligence",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
:root { --ri-ink:#17243a; --ri-muted:#68778d; --ri-line:#e7ebf2; --ri-blue:#3157a4; }
.block-container {max-width: 1440px; padding-top: 1.5rem; padding-bottom: 3rem;}
[data-testid="stSidebar"] {border-right:1px solid var(--ri-line);}
[data-testid="stMetric"] {background:#fff; border:1px solid var(--ri-line); border-radius:14px; padding:14px 16px; box-shadow:0 2px 8px rgba(20,35,60,.035);}
[data-testid="stMetricLabel"] {color:#65748a;}
.ri-hero {padding:28px 30px; border-radius:18px; color:white; background:linear-gradient(115deg,#14233f 0%,#294b83 65%,#4969a6 100%); margin:4px 0 22px 0;}
.ri-hero h1 {font-size:30px; font-weight:700; letter-spacing:-.5px; margin:0;}
.ri-hero p {color:#d9e4f5; font-size:15px; margin:8px 0 0 0;}
.ri-eyebrow {font-size:11px; text-transform:uppercase; letter-spacing:1.5px; color:#9fb8e3; font-weight:700; margin-bottom:8px;}
.ri-section {font-weight:650; font-size:19px; color:#1c2b43; margin:14px 0 6px;}
.ri-muted {color:#718096; font-size:13px;}
.ri-panel {border:1px solid var(--ri-line); border-radius:14px; padding:16px 18px; background:#fff;}
div.stButton > button[kind="primary"] {border-radius:10px; font-weight:600; padding:.6rem 1rem;}
.stTabs [data-baseweb="tab-list"] {gap:8px;}
.stTabs [data-baseweb="tab"] {border-radius:8px 8px 0 0; padding:9px 15px;}
</style>
""", unsafe_allow_html=True)

if "analysis" not in st.session_state:
    st.session_state.analysis = None
if "nav_page" not in st.session_state:
    st.session_state.nav_page = "Overview"

with st.sidebar:
    st.markdown("## 🧭 ResumeIQ")
    st.caption("RESUME INTELLIGENCE PLATFORM")
    st.divider()
    page_options = ["Overview", "Analyze Resume", "About"]
    default_index = page_options.index(st.session_state.nav_page) if st.session_state.nav_page in page_options else 0
    page = st.radio("WORKSPACE", page_options, index=default_index, label_visibility="visible")
    st.session_state.nav_page = page
    st.divider()
    st.markdown("**Analysis workflow**")
    st.caption("01  Upload resume")
    st.caption("02  Extract profile")
    st.caption("03  Review ATS signals")
    st.caption("04  Improve & export")
    st.divider()
    st.caption("Privacy note")
    st.caption("Files are processed in the active app session.")

def hero(title, subtitle, eyebrow="RESUME INTELLIGENCE"):
    st.markdown(f'<div class="ri-hero"><div class="ri-eyebrow">{eyebrow}</div><h1>{title}</h1><p>{subtitle}</p></div>', unsafe_allow_html=True)

def render_result(result):
    parsed=result["parsed"]
    score=result["score"]
    personal=parsed.get("personal_information",{})
    skills=parsed.get("skills",{})
    skill_count=parsed.get("skill_count",0)
    experience=parsed.get("experience_records",[])
    projects=parsed.get("project_records",[])
    confidence=result.get("confidence",0)

    st.markdown("### Candidate snapshot")
    c1,c2,c3,c4,c5=st.columns(5)
    c1.metric("ATS readiness",f'{score.get("total",0)}/100',score_label(score.get("total",0)))
    c2.metric("Skills identified",skill_count)
    c3.metric("Experience entries",len(experience))
    c4.metric("Projects",len(projects))
    c5.metric("Extraction signals",f"{confidence}%")

    tabs=st.tabs(["Profile","Skills","Experience","Projects & Education","Recommendations","Deep Analytics","AI Review","Export"])
    with tabs[0]:
        left,right=st.columns([1.1,1])
        with left:
            st.markdown("#### Personal information")
            details=[
                ("Full name",personal.get("name")),
                ("Email",personal.get("email")),
                ("Phone",personal.get("phone")),
                ("Location",personal.get("location")),
                ("LinkedIn",personal.get("linkedin")),
                ("GitHub",personal.get("github")),
                ("Portfolio",personal.get("portfolio")),
            ]
            st.dataframe(pd.DataFrame([{"Field":k,"Extracted value":v or "Not detected"} for k,v in details]),hide_index=True,use_container_width=True)
        with right:
            st.markdown("#### Resume quality")
            st.progress(max(0,min(100,confidence))/100)
            st.write(f"**{confidence}% extraction signal coverage**")
            st.caption("This indicates how many expected data points were detected. It does not verify factual accuracy.")
            st.markdown("#### Section detection")
            for section,detected in parsed.get("section_presence",{}).items():
                st.write(("✓" if detected else "—")+f"  {section.title()}")
    with tabs[1]:
        st.markdown("#### Skills inventory")
        st.caption(f"{skill_count} skills detected across {len(skills)} categories.")
        if skills:
            cols=st.columns(2)
            for idx,(category,items) in enumerate(skills.items()):
                with cols[idx%2]:
                    st.markdown(f"**{category}**")
                    st.write(" · ".join(items))
        else:
            st.info("No skills matched the current taxonomy. Review the raw text and add missing skill terms to the taxonomy if appropriate.")
    with tabs[2]:
        st.markdown("#### Professional experience")
        if experience:
            for idx,item in enumerate(experience):
                with st.container(border=True):
                    title=item.get("role") or "Role not identified"
                    company=item.get("company") or "Organization not identified"
                    st.markdown(f"**{title}**  \n{company}")
                    if item.get("duration"): st.caption(item["duration"])
                    if item.get("description"): st.write(item["description"])
                    elif item.get("bullets"):
                        for bullet in item["bullets"]: st.write("• "+bullet)
        else:
            st.warning("No structured experience entries were detected. Check whether the resume uses a standard Experience or Employment heading.")
    with tabs[3]:
        left,right=st.columns(2)
        with left:
            st.markdown("#### Projects")
            if projects:
                for item in projects:
                    with st.container(border=True):
                        st.markdown(f"**{item.get('name','Project')}**")
                        if item.get("technologies"): st.caption(" · ".join(item["technologies"]))
                        if item.get("description"): st.write(item["description"])
            else: st.info("No project entries detected.")
        with right:
            st.markdown("#### Education")
            for item in parsed.get("education",[]): st.write("• "+item)
            if not parsed.get("education"): st.info("No education entries detected.")
            st.markdown("#### Certifications")
            for item in parsed.get("certifications",[]): st.write("• "+item)
            if not parsed.get("certifications"): st.caption("No certifications detected.")
    with tabs[4]:
        st.markdown("#### Prioritized improvement plan")
        for i,item in enumerate(result.get("recommendations",[]),1):
            with st.container(border=True):
                col_a,col_b=st.columns([5,1])
                col_a.markdown(f"**{i}. {item['title']}**")
                col_a.write(item["detail"])
                col_b.caption("PRIORITY")
                col_b.markdown(f"**{item.get('priority','Medium')}**")
    with tabs[5]:
        analytics=result["analytics"]
        col_a,col_b=st.columns(2)
        with col_a:
            st.markdown("#### Resume section coverage")
            df=pd.DataFrame({"Section":list(analytics["section_counts"].keys()),"Entries":list(analytics["section_counts"].values())})
            st.plotly_chart(px.pie(df,names="Section",values="Entries",hole=.48),use_container_width=True)
        with col_b:
            st.markdown("#### ATS category performance")
            score_df=pd.DataFrame([{"Category":k,"Score":v} for k,v in score["breakdown"].items()])
            st.plotly_chart(px.bar(score_df,x="Score",y="Category",orientation="h",range_x=[0,20]),use_container_width=True)
        word_count=analytics.get("word_count",0)
        w1,w2,w3=st.columns(3)
        w1.metric("Word count",word_count)
        w2.metric("Unique skill terms",skill_count)
        w3.metric("Detected sections",sum(parsed.get("section_presence",{}).values()))
    with tabs[6]:
        st.markdown("#### AI-assisted review")
        st.caption("Optional local Ollama integration. This feature requires Ollama to be running on the same machine as the app.")
        if st.button("Generate AI review",key="generate_ai_review"):
            with st.spinner("Generating review with local Ollama..."):
                review=generate_ai_review(parsed,score,result.get("job_description",""))
            st.markdown(review)
    with tabs[7]:
        st.markdown("#### Download your analysis")
        export={
            "filename":result["filename"],
            "parsed_resume":parsed,
            "ats_readiness":score,
            "recommendations":result.get("recommendations",[]),
            "extraction_confidence":confidence,
        }
        st.download_button("Download structured JSON",json.dumps(export,indent=2,ensure_ascii=False),file_name="resumeiq_analysis.json",mime="application/json",use_container_width=True)
        with st.expander("Review extracted source text"):
            st.text_area("Extracted text",result["text"],height=280)

if page=="Overview":
    hero("A clearer view of every resume.","Turn unstructured resumes into structured candidate insights and practical improvement actions.","RESUMEIQ WORKSPACE")
    st.markdown("### Your resume analysis workspace")
    col1,col2=st.columns([1.5,1])
    with col1:
        st.markdown("#### From document to actionable insight")
        st.write("ResumeIQ extracts candidate information, evaluates common ATS-readiness signals, and highlights areas that may need attention.")
        if st.button("Start a new analysis",type="primary",use_container_width=True):
            st.session_state.nav_page="Analyze Resume"
            st.rerun()
    with col2:
        st.markdown("#### Analysis modules")
        for label in ["Structured resume extraction","Skills and experience mapping","Explainable ATS-readiness scoring","Improvement recommendations","Visual content analytics","Downloadable analysis report"]:
            st.write("✓  "+label)
    st.divider()
    st.markdown("### Latest analysis")
    if st.session_state.analysis:
        result=st.session_state.analysis
        c1,c2,c3,c4=st.columns(4)
        c1.metric("Last resume score",f'{result["score"]["total"]}/100')
        c2.metric("Skills",result["parsed"]["skill_count"])
        c3.metric("Experience",len(result["parsed"]["experience_records"]))
        c4.metric("Projects",len(result["parsed"]["project_records"]))
        if st.button("Open latest analysis"):
            st.session_state.nav_page="Analyze Resume"
            st.rerun()
    else:
        st.info("No resume has been analyzed in this session yet. Select **Analyze Resume** to upload a document.")
    st.caption("Scoring note: ATS readiness is a heuristic assessment of document structure and content signals. It is not an employer ATS result or a prediction of hiring outcomes.")

elif page=="Analyze Resume":
    hero("Analyze a resume.","Upload a candidate resume and review its extracted profile, ATS-readiness signals and improvement opportunities.","ANALYSIS WORKSPACE")
    upload_col,context_col=st.columns([1.1,1])
    with upload_col:
        uploaded=st.file_uploader("Upload resume",type=["pdf","docx","txt","md","rtf"],help="PDF, DOCX, TXT, Markdown or RTF. Text-based documents work best.")
    with context_col:
        job_description=st.text_area("Target job description (optional)",height=120,placeholder="Paste the job description to assess keyword alignment...")
    if uploaded:
        st.caption(f"Selected file: **{uploaded.name}** · {uploaded.size/1024:.1f} KB")
    if st.button("Run resume analysis",type="primary",disabled=uploaded is None,use_container_width=True):
        if uploaded.size>10*1024*1024:
            st.error("File exceeds the 10 MB upload limit. Please upload a smaller file.")
        else:
            try:
                with st.spinner("Extracting document and building candidate profile..."):
                    extracted_text,embedded_links=extract_document(uploaded)
                    if len(extracted_text.strip())<40:
                        raise ValueError("Very little text was extracted. This may be a scanned or image-only document.")
                    parsed=parse_resume(extracted_text,embedded_links=embedded_links)
                    score=calculate_score(parsed,job_description)
                    confidence=calculate_extraction_confidence(parsed)
                    recommendations=generate_recommendations(parsed,score,job_description)
                    analytics=build_analytics(parsed,score)
                    st.session_state.analysis={
                        "filename":uploaded.name,"parsed":parsed,"score":score,"text":extracted_text,
                        "confidence":confidence,"recommendations":recommendations,"analytics":analytics,
                        "job_description":job_description,
                    }
                st.success("Resume analysis completed.")
            except Exception as exc:
                st.error(f"Could not process this document: {exc}")
    if st.session_state.analysis:
        st.divider()
        render_result(st.session_state.analysis)

elif page=="About":
    hero("Built for clearer resume decisions.","A practical resume parsing and analysis tool with transparent scoring and reviewable outputs.","ABOUT RESUMEIQ")
    st.markdown("### Product capabilities")
    c1,c2,c3=st.columns(3)
    c1.markdown("**Document intelligence**")
    c1.write("Extracts text and organizes key candidate details into structured sections.")
    c2.markdown("**ATS-readiness signals**")
    c2.write("Scores common resume content signals and explains the category-level breakdown.")
    c3.markdown("**Actionable insights**")
    c3.write("Surfaces improvement suggestions and visual summaries for review.")
    st.divider()
    st.markdown("### Responsible use")
    st.warning("ResumeIQ is a decision-support prototype, not a hiring system or a substitute for human review. Extraction may be incomplete, especially with complex columns, text boxes, scanned files or unusual formatting. Validate all details before acting on the report.")
    st.markdown("### Technology")
    st.write("Python · Streamlit · PyMuPDF · python-docx · Pandas · Plotly · Optional Ollama")
