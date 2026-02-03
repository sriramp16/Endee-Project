import os
import requests
import json
from typing import List, Dict, Any

class EndeeVectorStore:
    def __init__(self, host: str = "localhost", port: int = 8080, collection_name: str = "research_papers"):
        self.base_url = f"http://{host}:{port}"
        self.collection = collection_name
        self.headers = {"Content-Type": "application/json"}
        self._ensure_collection()

    def _ensure_collection(self):
        try:
            requests.post(f"{self.base_url}/collections", json={"name": self.collection}, headers=self.headers)
        except Exception:
            pass 

    def insert(self, vectors: List[List[float]], documents: List[Dict]):
        payload = []
        for vec, doc in zip(vectors, documents):
            payload.append({
                "vector": vec,
                "metadata": doc["metadata"],
                "text": doc["text"],
                "id": doc["id"]
            })
        
        response = requests.post(
            f"{self.base_url}/collections/{self.collection}/insert",
            json={"items": payload},
            headers=self.headers
        )
        return response.status_code == 200

    def search(self, query_vector: List[float], top_k: int = 5) -> List[Dict]:
        response = requests.post(
            f"{self.base_url}/collections/{self.collection}/search",
            json={
                "vector": query_vector,
                "top_k": top_k
            },
            headers=self.headers
        )
        
        if response.status_code == 200:
            results = response.json()
            return [
                {
                    "text": item.get("text", ""),
                    "metadata": item.get("metadata", {}),
                    "score": item.get("score", 0.0)
                }
                for item in results.get("results", [])
            ]
        return []
