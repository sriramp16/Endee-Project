from pydantic import BaseModel
from typing import List, Optional

class ProcessRequest(BaseModel):
    filename: str

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

class SearchResult(BaseModel):
    text: str
    score: float
    metadata: dict

class ChatRequest(BaseModel):
    message: str
    history: List[dict] = []

class ChatResponse(BaseModel):
    answer: str
    citations: List[dict]
