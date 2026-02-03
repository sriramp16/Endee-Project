import os
import shutil
from typing import List
from fastapi import FastAPI, UploadFile, File, HTTPException
from contextlib import asynccontextmanager
from dotenv import load_dotenv

from backend.models import ProcessRequest, SearchRequest, SearchResult, ChatRequest, ChatResponse
from backend.ingestion import extract_text_from_pdf, chunk_text
from backend.embeddings import embedding_model
from backend.vector_store import EndeeVectorStore
from backend.rag import RAGPipeline

load_dotenv()

vector_store = None
rag_pipeline = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global vector_store, rag_pipeline
    host = os.getenv("ENDEE_HOST", "localhost")
    port = int(os.getenv("ENDEE_PORT", "8080"))
    groq_key = os.getenv("GROQ_API_KEY")
    
    vector_store = EndeeVectorStore(host=host, port=port)
    rag_pipeline = RAGPipeline(api_key=groq_key)
    yield

app = FastAPI(title="Endee RAG API", lifespan=lifespan)

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    content = await file.read()
    
    pages = extract_text_from_pdf(content, file.filename)
    if not pages:
        raise HTTPException(status_code=400, detail="Could not extract text from PDF")
        
    chunks = chunk_text(pages)
    
    texts = [c["text"] for c in chunks]
    embeddings = embedding_model.generate_batch(texts)
    
    success = vector_store.insert(embeddings, chunks)
    
    return {"message": f"Processed {len(chunks)} chunks from {file.filename}", "chunks": len(chunks)}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    query_vec = embedding_model.generate(request.message)
    
    results = vector_store.search(query_vec, top_k=5)
    
    response = rag_pipeline.generate_answer(request.message, results)
    
    return response

@app.get("/health")
def health():
    return {"status": "ok"}
