from knowvault.retriever import Retriever
def test_retrieval():
    r=Retriever();r.rebuild([{"source":"a.txt","chunk_id":1,"text":"Python FastAPI backend"},{"source":"b.txt","chunk_id":1,"text":"machine learning models"}])
    assert r.search("FastAPI Python",1)[0]["source"]=="a.txt"
