# ResumeIQ

AI-powered resume parsing and optimization platform built with Streamlit.

## Day 1 features
- PDF and DOCX text extraction
- Contact detail extraction
- Rule-based skill categorization
- Education, experience, project and certification extraction
- Initial transparent heuristic score
- JSON export

## Run locally
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

Note: The Day 1 parser uses a curated skill taxonomy and conventional section headings. It is a foundation, not a production-grade ATS parser. Scanned PDFs require OCR, which is not included yet.
