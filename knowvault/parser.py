from io import BytesIO
from pathlib import Path
from pypdf import PdfReader
from docx import Document

def extract_text(filename,content):
    ext=Path(filename).suffix.lower()
    if ext in {".txt",".md"}: return content.decode("utf-8",errors="ignore")
    if ext==".pdf":
        return "\n".join((p.extract_text() or "") for p in PdfReader(BytesIO(content)).pages)
    if ext==".docx":
        return "\n".join(p.text for p in Document(BytesIO(content)).paragraphs)
    raise ValueError("Unsupported document type")
