def chunk_text(text,chunk_size=900,overlap=120):
    clean=" ".join(text.split())
    if not clean:return []
    out=[];start=0
    while start<len(clean):
        end=min(len(clean),start+chunk_size)
        out.append(clean[start:end])
        if end==len(clean):break
        start=max(end-overlap,start+1)
    return out
