from knowvault.chunker import chunk_text
def test_chunker():
    x=chunk_text("hello "*500,100,20);assert len(x)>1 and all(x)
