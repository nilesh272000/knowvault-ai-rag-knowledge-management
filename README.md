# KnowVault AI — RAG Knowledge Management System

Production-oriented RAG knowledge management assistant.

## Features
- TXT, Markdown, PDF and DOCX ingestion
- Chunking with metadata
- TF-IDF retrieval with cosine similarity
- Optional OpenAI grounded answer generation
- Source-aware answers
- FastAPI REST API + Swagger
- Browser UI
- SQLite document catalog
- Knowledge-base statistics
- Tests and sample knowledge
- No Docker dependency and no secrets included

## Architecture
Documents → Parser → Chunker → Retriever → Context Builder → LLM → Answer + Sources

## Run
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python -m uvicorn app:app --reload --port 8080
```
Open http://127.0.0.1:8080 and `/docs` for Swagger.

`OPENAI_API_KEY` is optional. Without it, the system operates in retrieval/demo mode.

## Portfolio Positioning
Demonstrates practical RAG engineering: ingestion, chunking, retrieval, grounded generation, source attribution, API design and operational separation between ingestion and query flows.

Educational portfolio project. Do not upload confidential or sensitive documents.
