from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from knowvault.service import KnowledgeService
from knowvault.models import QueryRequest

app=FastAPI(title="KnowVault AI",version="1.0.0")
app.mount("/static",StaticFiles(directory="static"),name="static")
templates=Jinja2Templates(directory="templates")
service=KnowledgeService()

@app.get("/",response_class=HTMLResponse)
def home(request:Request):
    return templates.TemplateResponse("index.html",{"request":request})

@app.get("/health")
def health():
    return {"status":"healthy","documents":service.document_count(),"chunks":service.chunk_count()}

@app.get("/documents")
def documents(): return service.documents()

@app.post("/documents/upload")
async def upload(file:UploadFile=File(...)):
    if not file.filename: raise HTTPException(400,"Filename is required")
    if Path(file.filename).suffix.lower() not in {".txt",".md",".pdf",".docx"}:
        raise HTTPException(400,"Supported types: TXT, MD, PDF, DOCX")
    return service.ingest(file.filename,await file.read())

@app.post("/query")
def query(payload:QueryRequest): return service.answer(payload.query,payload.top_k)

@app.delete("/documents/{name}")
def delete_document(name:str): return service.delete_document(name)
