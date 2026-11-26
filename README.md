# ResumeIQ – AI-Powered Resume Parsing and ATS Analysis Platform

**ResumeIQ** is an AI-powered resume parsing and analysis platform built with Python and Streamlit. It extracts structured information from resumes, evaluates resume quality using ATS-oriented scoring techniques, and provides actionable recommendations to help candidates improve their resumes.

The platform is designed to simplify resume evaluation by combining automated document parsing, skill extraction, resume scoring, job-description matching, and AI-assisted feedback in one interactive application.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [System Architecture](#system-architecture)
- [Project Structure](#project-structure)
- [Installation and Setup](#installation-and-setup)
- [Running the Application](#running-the-application)
- [Application Modules](#application-modules)
- [AI-Powered Resume Review](#ai-powered-resume-review)
- [ATS Scoring Methodology](#ats-scoring-methodology)
- [Supported File Formats](#supported-file-formats)
- [Deployment](#deployment)
- [Security and Privacy](#security-and-privacy)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

---

## Project Overview

Recruitment processes often involve reviewing large numbers of resumes. Manually evaluating each resume can be time-consuming, and candidates may struggle to understand whether their resumes effectively communicate their qualifications.

ResumeIQ addresses these challenges by providing an automated resume analysis workflow.

Users can upload a resume and receive structured information about their:

- Contact information
- Technical and professional skills
- Work experience
- Educational qualifications
- Projects
- Certifications
- Resume completeness and ATS-oriented quality

Users can also provide a job description to evaluate keyword alignment and identify areas where their resumes could be improved.

### Project Objectives

1. Automate resume information extraction.
2. Convert unstructured resume documents into structured data.
3. Evaluate resumes using ATS-oriented scoring criteria.
4. Identify relevant skills and missing job-description keywords.
5. Provide actionable resume improvement recommendations.
6. Integrate local Large Language Models for AI-assisted resume feedback.

---

## Key Features

### 1. Automated Resume Parsing

Extracts relevant information from uploaded resume documents and organizes it into structured sections.

Information includes:

- Personal and contact details
- Skills and technical competencies
- Professional experience
- Educational qualifications
- Projects and achievements
- Certifications

### 2. ATS Resume Scoring

Evaluates resumes using a rule-based scoring approach.

The analysis can consider:

- Resume structure and completeness
- Contact information
- Skills coverage
- Professional experience
- Educational details
- Projects and certifications
- Content organization

The resulting score helps users identify potential areas for improvement.

**Note:** ResumeIQ provides an estimated ATS-oriented score. It does not reproduce the proprietary scoring algorithms of commercial Applicant Tracking Systems.

### 3. Job Description Matching

Users can enter a target job description to compare its keywords and requirements against the information extracted from their resumes.

The analysis helps identify:

- Matching skills
- Missing keywords
- Relevant qualifications
- Potential skill gaps
- Areas requiring better alignment

### 4. AI-Powered Resume Review

ResumeIQ supports optional integration with a locally running Ollama model.

The AI review can provide additional feedback on:

- Resume content
- Professional presentation
- Skills representation
- Experience descriptions
- Improvement opportunities

The AI review is an additional analysis layer and is separate from the rule-based ATS scoring system.

### 5. Interactive Dashboard

The Streamlit interface presents resume analysis results in an organized and interactive format.

Depending on the available analysis data, the dashboard can display:

- Overall resume score
- Score breakdown
- Extracted resume information
- Skill distribution
- Resume analysis summaries
- Improvement recommendations

### 6. Resume Data Export

Supports exporting structured resume analysis information in JSON format for further processing and integration.

### 7. Deep Analytics

Provides visual insights into extracted resume information and scoring results through interactive analytical visualizations.

---

## Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Frontend / UI | Streamlit |
| Document Processing | PyMuPDF, python-docx |
| Data Processing | Pandas |
| Data Visualization | Plotly |
| AI Integration | Ollama |
| LLM | Llama 3.2 (optional local model) |
| Data Format | JSON |
| Version Control | Git and GitHub |

*The exact dependencies may vary according to the installed project configuration.*

---

## System Architecture

ResumeIQ follows a modular architecture that separates document processing, information extraction, scoring, AI-assisted review, and dashboard presentation.

### Processing Workflow

```text
                 USER
                   |
                   v
          Upload Resume Document
                   |
                   v
          Streamlit Application
                   |
                   v
          Resume File Processing
                   |
                   v
           Text Extraction
                   |
                   v
          Resume Information Parser
                   |
          +--------+--------+
          |        |        |
          v        v        v
       Contact   Skills   Experience
       Details   Data     & Education
          |        |        |
          +--------+--------+
                   |
                   v
             Resume Scorer
                   |
          +--------+---------+
          |                  |
          v                  v
      ATS Analysis      Job Description
                           Matching
          |                  |
          +--------+---------+
                   |
                   v
             AI Resume Review
              (Optional)
                   |
                   v
           Analysis Dashboard
                   |
                   v
           Recommendations
                   |
                   v
              JSON Export
```

### Architecture Components

**1. User Interface Layer**

Provides the Streamlit interface for uploading resumes, entering job descriptions, and viewing analysis results.

**2. Document Processing Layer**

Extracts text from supported resume formats.

**3. Resume Parsing Layer**

Identifies and organizes relevant information from extracted resume text.

**4. Resume Scoring Layer**

Evaluates resume completeness and calculates ATS-oriented scores.

**5. AI Integration Layer**

Connects to a locally running Ollama model for additional resume feedback.

**6. Presentation and Analytics Layer**

Displays extracted information, scoring results, charts, and recommendations.

---

## Project Structure

The following is the intended high-level organization. Adjust the names to match the actual files in your repository.

```text
Resume_Parsing_System/
│
├── app.py
│
├── modules/
│   ├── __init__.py
│   ├── resume_parser.py
│   ├── resume_scorer.py
│   └── ai_assistant.py
│
├── assets/
│
├── requirements.txt
│
├── README.md
│
├── .gitignore
│
└── .streamlit/
    └── config.toml
```

### Important Files

| File | Responsibility |
|---|---|
| `app.py` | Main Streamlit application |
| `resume_parser.py` | Resume text processing and information extraction |
| `resume_scorer.py` | ATS-oriented resume scoring |
| `ai_assistant.py` | Optional Ollama-based AI review |
| `requirements.txt` | Python dependency list |
| `.gitignore` | Excludes unnecessary and sensitive files |

---

## Installation and Setup

### Prerequisites

Before installing ResumeIQ, ensure that you have:

- Python 3.10 or later
- Git
- pip
- A modern web browser

For AI-assisted resume review, install Ollama separately.

### Step 1: Clone the Repository

```bash
git clone https://github.com/Naveengowtham2003/Resume_Parsing_System.git
```

Navigate into the project directory:

```bash
cd Resume_Parsing_System
```

### Step 2: Create a Virtual Environment

```bash
python -m venv .venv
```

### Step 3: Activate the Virtual Environment

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**

```cmd
.venv\Scripts\activate.bat
```

**Linux / macOS:**

```bash
source .venv/bin/activate
```

### Step 4: Install Dependencies

```bash
python -m pip install --upgrade pip
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Application

Once the dependencies are installed, start the Streamlit application:

```bash
streamlit run app.py
```

The application will normally become available at:

```text
http://localhost:8501
```

### Basic Usage

1. Open ResumeIQ in your browser.
2. Upload your resume using the file uploader.
3. Allow the application to extract and process the document.
4. Review the extracted personal, educational, professional, and skills information.
5. Check the ATS-oriented resume score and its breakdown.
6. Optionally enter a job description to evaluate keyword alignment.
7. Review the recommendations.
8. Use the AI review feature if local Ollama integration is configured.
9. Export the structured analysis when required.

---

## Application Modules

### Resume Parser

The resume parser is responsible for extracting information from uploaded documents.

Its processing workflow includes:

1. Reading the uploaded document.
2. Extracting its textual content.
3. Identifying relevant resume sections.
4. Extracting structured information.
5. Preparing the extracted information for scoring and presentation.

### Resume Scorer

The scoring module evaluates the extracted resume information using predefined criteria.

It provides an overall score and supporting category-level results.

The scoring system is intended to help candidates understand resume completeness and identify areas that may need attention.

### AI Assistant

The AI assistant provides optional LLM-powered resume feedback.

It is designed to complement the deterministic parsing and scoring modules rather than replace them.

### Dashboard

The dashboard brings together the outputs of the different modules and presents them through an interactive interface.

---

## AI-Powered Resume Review

ResumeIQ can integrate with Ollama to run a Large Language Model locally.

### Step 1: Install Ollama

Download Ollama from:

https://ollama.com/

### Step 2: Download the Model

For the configured Llama 3.2 model, run:

```bash
ollama pull llama3.2
```

### Step 3: Start Ollama

```bash
ollama serve
```

If Ollama is already running as a background service, starting another server may report that the port is already in use.

### Step 4: Verify the Ollama Service

Open PowerShell and execute:

```powershell
Invoke-RestMethod http://127.0.0.1:11434/api/tags
```

The service should return information about the locally available models.

### Step 5: Run ResumeIQ

In another terminal, activate the project virtual environment and launch:

```bash
streamlit run app.py
```

### Optional Configuration

The AI assistant can be configured using environment variables, if supported by the installed version:

| Variable | Purpose | Example |
|---|---|---|
| `OLLAMA_BASE_URL` | Ollama server address | `http://127.0.0.1:11434` |
| `OLLAMA_MODEL` | Model identifier | `llama3.2` |
| `OLLAMA_TIMEOUT` | Request timeout in seconds | `600` |

Ollama is optional. Core parsing and scoring functionality should be treated separately from the local AI review dependency.

---

## ATS Scoring Methodology

ResumeIQ uses an application-defined scoring approach to evaluate resume quality.

The analysis considers different aspects of the resume, including:

- Contact information completeness
- Skills information
- Work experience
- Educational qualifications
- Projects and certifications
- Resume content and organization

The application combines these factors into an overall score and presents supporting category-level feedback.

### Important Limitations

- The score is an estimate, not an official ATS result.
- Different employers use different ATS products and configurations.
- Keyword matching does not guarantee job suitability.
- A high score does not guarantee an interview or selection.
- AI-generated feedback may occasionally be inaccurate and should be reviewed.

---

## Supported File Formats

ResumeIQ is designed to process common resume document formats, subject to the installed document-processing dependencies.

| Format | Extension |
|---|---|
| PDF | `.pdf` |
| Microsoft Word | `.docx` |
| Plain Text | `.txt` |
| Markdown | `.md` |
| Rich Text Format | `.rtf` |

Scanned PDFs may require OCR support if their content is not available as extractable text. Legacy `.doc` files may require an additional conversion or extraction mechanism.

---

## Deployment

ResumeIQ can be deployed as a Streamlit application.

### Local Deployment

Run:

```bash
streamlit run app.py
```

### Streamlit Community Cloud

A typical deployment workflow is:

1. Push the project to a GitHub repository.
2. Sign in to Streamlit Community Cloud.
3. Connect the GitHub repository.
4. Select the repository and branch.
5. Specify `app.py` as the application entry point.
6. Configure any required dependencies and application settings.
7. Deploy the application.

**Important:** A locally installed Ollama service and its downloaded model are not automatically available on Streamlit Community Cloud. The AI review functionality requires a separately hosted, securely accessible inference service or must be disabled in that environment.

---

## Security and Privacy

Resume documents can contain personally identifiable information. Handle uploaded files responsibly.

Recommended practices:

- Do not commit real resumes or personal documents to GitHub.
- Never commit API keys, credentials, or `.env` files.
- Exclude virtual environments and model binaries from version control.
- Avoid logging sensitive resume content.
- Inform users how uploaded files and extracted information are processed.
- Use secure endpoints when connecting to external AI services.

ResumeIQ should not be considered a secure document-storage platform unless additional storage, access-control, and data-retention mechanisms are implemented.

---

## Future Enhancements

Potential improvements for future versions include:

- Advanced NLP-based resume section classification.
- Named Entity Recognition for more accurate information extraction.
- Semantic job-description matching using sentence embeddings.
- Vector database integration for semantic retrieval.
- Retrieval-Augmented Generation (RAG) for contextual resume recommendations.
- Multi-resume comparison and candidate ranking.
- Resume improvement suggestions tailored to specific job roles.
- OCR support for scanned documents.
- Additional document export formats.
- Cloud-hosted LLM integration.
- User authentication and analysis history.
- Automated resume formatting and rewriting assistance.

---

## Contributing

Contributions, suggestions, and bug reports are welcome.

To contribute:

1. Fork the repository.
2. Create a feature branch.

```bash
git checkout -b feature/your-feature-name
```

3. Implement your changes.
4. Commit your changes.

```bash
git commit -m "Add: describe your feature"
```

5. Push your branch.

```bash
git push origin feature/your-feature-name
```

6. Open a Pull Request.

---

## License

This project is currently available for personal and educational use.

A formal open-source license should be added to the repository before specifying permissions for redistribution, modification, or commercial use.

---

## Author

**Naveen Gowtham K T**

B.E. Computer Science and Engineering

**Areas of Interest:**
- Artificial Intelligence and Machine Learning
- Generative AI and Large Language Models
- Python Development
- Natural Language Processing
- AI-Powered Applications

### Project

**ResumeIQ – AI-Powered Resume Parsing and ATS Analysis Platform**

GitHub Repository:  
https://github.com/Naveengowtham2003/Resume_Parsing_System

---

*ResumeIQ — Making Resume Analysis Smarter, Structured, and More Accessible.*
