from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
class Retriever:
    def __init__(self):self.items=[];self.vectorizer=None;self.matrix=None
    def rebuild(self,items):
        self.items=items
        if not items:self.vectorizer=self.matrix=None;return
        self.vectorizer=TfidfVectorizer(stop_words="english",ngram_range=(1,2),max_features=8000)
        self.matrix=self.vectorizer.fit_transform([x["text"] for x in items])
    def search(self,query,k=5):
        if not self.items or self.vectorizer is None:return []
        scores=cosine_similarity(self.vectorizer.transform([query]),self.matrix)[0]
        order=scores.argsort()[::-1][:k]
        return [{**self.items[i],"score":round(float(scores[i]),4)} for i in order if scores[i]>0]
