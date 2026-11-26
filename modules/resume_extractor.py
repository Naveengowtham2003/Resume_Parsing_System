
from pathlib import Path
import re
from io import BytesIO

def _read_pdf(data: bytes):
    import fitz
    document=fitz.open(stream=data,filetype="pdf")
    text_parts=[]
    links=[]
    for page in document:
        text_parts.append(page.get_text("text",sort=True))
        for item in page.get_links():
            uri=item.get("uri")
            if uri and uri not in links:
                links.append(uri)
    return "\n".join(text_parts),links

def _read_docx(data: bytes):
    from docx import Document
    from docx.text.paragraph import Paragraph
    from docx.table import Table
    document=Document(BytesIO(data))
    parts=[]
    body=document.element.body
    # Preserve body order and extract both ordinary paragraphs and tables.
    for child in body.iterchildren():
        tag=child.tag.split("}")[-1]
        if tag=="p":
            paragraph=Paragraph(child,document)
            if paragraph.text.strip():
                parts.append(paragraph.text.strip())
        elif tag=="tbl":
            table=Table(child,document)
            for row in table.rows:
                cells=[]
                for cell in row.cells:
                    value=" / ".join(x.strip() for x in cell.text.splitlines() if x.strip())
                    if value: cells.append(value)
                if cells: parts.append(" | ".join(cells))
    for section in document.sections:
        for paragraph in section.header.paragraphs:
            if paragraph.text.strip(): parts.insert(0,paragraph.text.strip())
        for paragraph in section.footer.paragraphs:
            if paragraph.text.strip(): parts.append(paragraph.text.strip())
    # Extract only text inside OOXML text boxes (not every paragraph a second time).
    xml=document.element.xml
    textbox_blocks=re.findall(r"<w:txbxContent\b[^>]*>(.*?)</w:txbxContent>",xml,re.S)
    for block in textbox_blocks:
        values=re.findall(r"<w:t\b[^>]*>(.*?)</w:t>",block,re.S)
        if values:
            textbox=" ".join(re.sub(r"&amp;","&",v) for v in values).strip()
            if textbox and textbox not in parts:
                parts.append(textbox)
    links=[]
    for rel in document.part.rels.values():
        if "hyperlink" in rel.reltype and rel.target_ref not in links:
            links.append(rel.target_ref)
    return "\n".join(parts),links

def extract_document(uploaded_file):
    filename=(getattr(uploaded_file,"name","") or "").lower()
    data=uploaded_file.getvalue()
    suffix=Path(filename).suffix
    if suffix==".pdf":
        text,links=_read_pdf(data)
    elif suffix==".docx":
        text,links=_read_docx(data)
    elif suffix in {".txt",".md"}:
        text=data.decode("utf-8",errors="ignore")
        links=[]
    elif suffix==".rtf":
        raw=data.decode("utf-8",errors="ignore")
        text=re.sub(r"\\'[0-9a-fA-F]{2}"," ",raw)
        text=re.sub(r"\\[a-zA-Z]+-?\d* ?"," ",text)
        text=text.replace("{"," ").replace("}"," ")
        links=[]
    elif suffix==".doc":
        raise ValueError("Legacy .doc files are not supported directly. Open the file in Word and save it as .docx or PDF.")
    else:
        raise ValueError("Unsupported file format. Upload PDF, DOCX, TXT, MD or RTF.")
    if not text or not text.strip():
        raise ValueError("No readable text was extracted. The document may be scanned or image-only.")
    return text,links

def extract_text(uploaded_file):
    return extract_document(uploaded_file)[0]
