from sentence_transformers import SentenceTransformer
import os

class EmbeddingModel:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def generate(self, text: str) -> list[float]:
        if not text or not text.strip():
            return []
        embeddings = self.model.encode(text)
        return embeddings.tolist()

    def generate_batch(self, texts: list[str]) -> list[list[float]]:
        valid_texts = [t for t in texts if t and t.strip()]
        if not valid_texts:
            return []
        embeddings = self.model.encode(valid_texts)
        return embeddings.tolist()

embedding_model = EmbeddingModel()
