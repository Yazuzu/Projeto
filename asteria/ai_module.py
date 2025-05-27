from sentence_transformers import SentenceTransformer

class AIModel:
    def _init_(self):
        self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

    def encode(self, text):
        return self.model.encode(text)

    def batch_encode(self, texts):
        return self.model.encode(texts, show_progress_bar=False)

ai=AIModel()