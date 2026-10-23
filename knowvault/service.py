import os,json
from pathlib import Path
from .parser import extract_text
from .chunker import chunk_text
from .retriever import Retriever
from .store import Catalog
INDEX=Path("data/index/chunks.json");INDEX.parent.mkdir(parents=True,exist_ok=True)
class KnowledgeService:
    def __init__(self):
        self.catalog=Catalog();self.retriever=Retriever();self.items=self._load();self.retriever.rebuild(self.items)
    def _load(self):
        try:return json.loads(INDEX.read_text(encoding="utf-8")) if INDEX.exists() else []
        except:return []
    def _save(self):INDEX.write_text(json.dumps(self.items,ensure_ascii=False,indent=2),encoding="utf-8")
    def ingest(self,filename,content):
        chunks=chunk_text(extract_text(filename,content))
        self.items=[x for x in self.items if x["source"]!=filename]
        self.items += [{"source":filename,"chunk_id":i+1,"text":c} for i,c in enumerate(chunks)]
        self.catalog.upsert(filename,len(chunks));self._save();self.retriever.rebuild(self.items)
        return {"message":"indexed","document":filename,"chunks":len(chunks)}
    def answer(self,query,top_k=5):
        hits=self.retriever.search(query,top_k)
        if not hits:return {"answer":"I could not find relevant information in the knowledge base.","sources":[]}
        context="\n\n".join(f"[{h['source']}#{h['chunk_id']}] {h['text']}" for h in hits)
        answer=self._generate(query,context)
        return {"answer":answer,"sources":[{"document":h["source"],"chunk":h["chunk_id"],"score":h["score"]} for h in hits]}
    def _generate(self,query,context):
        key=os.getenv("OPENAI_API_KEY")
        if not key:return "Demo retrieval result:\n\n"+context[:3500]
        try:
            from openai import OpenAI
            r=OpenAI(api_key=key).chat.completions.create(
                model=os.getenv("OPENAI_MODEL","gpt-4o-mini"),temperature=0.1,
                messages=[{"role":"system","content":"You are a grounded enterprise knowledge assistant. Answer only from context."},
                          {"role":"user","content":f"Question: {query}\n\nContext:\n{context}\n\nCite sources like [document#chunk]."}])
            return r.choices[0].message.content
        except Exception:return "LLM generation unavailable; retrieved evidence:\n\n"+context[:3500]
    def documents(self):return self.catalog.all()
    def delete_document(self,name):
        self.items=[x for x in self.items if x["source"]!=name];self.catalog.delete(name);self._save();self.retriever.rebuild(self.items)
        return {"message":"deleted","document":name}
    def document_count(self):return self.catalog.count()
    def chunk_count(self):return len(self.items)
