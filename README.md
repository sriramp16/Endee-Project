# Intelligent Research Assistant using RAG and Endee Vector Database

## Project Overview

The **Intelligent Research Assistant** is a production-ready AI system that enables users to interact with academic PDF documents through natural language queries.  
By leveraging **Retrieval Augmented Generation (RAG)**, the system provides **accurate, context-aware answers with page-level citations**, ensuring reliability and trust in the generated responses.

The application is built around the **Endee Vector Database**, which offers a high-performance C++ backend for fast and scalable semantic search.

---

## Problem Statement

Researchers and students often spend significant time manually searching through lengthy academic papers. Traditional keyword-based search fails to capture context, intent, and semantic meaning.

This project addresses the problem by:
- Understanding queries semantically rather than syntactically
- Retrieving only the most relevant document sections
- Generating concise answers grounded strictly in source documents
- Providing page-level citations to verify every response

---

## System Design and Technical Approach

The system follows a **Retrieval Augmented Generation (RAG)** architecture, separating retrieval from generation to ensure accuracy and transparency.

### High-Level Workflow
1. Academic PDFs are uploaded by the user
2. Text is extracted and split into overlapping chunks
3. Each chunk is converted into vector embeddings
4. Embeddings are stored and indexed in the Endee vector database
5. User queries are embedded and matched semantically
6. Relevant document context is retrieved
7. A large language model generates answers using retrieved context only

---

## Use of Endee Vector Database

**Endee** is used as the core vector storage and retrieval engine.

It was chosen for:
- **Performance**: Optimized C++ core enables low-latency nearest-neighbor search
- **Scalability**: Efficient handling of high-dimensional embeddings
- **Clean API**: Simple vector insertion and similarity search interface

### How Endee is Used
- Stores 384-dimensional embeddings generated from document chunks
- Indexes vectors along with metadata (file name, page number)
- Performs similarity search to retrieve the top relevant chunks for each query
- Acts as the retrieval backbone for the RAG pipeline

---

## Retrieval Augmented Generation (RAG) Pipeline

1. **Ingestion**  
   PDFs are processed and split into overlapping chunks  
   - Chunk size: 500 characters  
   - Overlap: 50 characters  

2. **Embedding**  
   Each chunk is converted into embeddings using  
   `sentence-transformers/all-MiniLM-L6-v2`

3. **Storage**  
   Embeddings and metadata are indexed into Endee

4. **Retrieval**  
   User queries are embedded and matched against stored vectors  
   Top 5 most relevant chunks are retrieved

5. **Generation**  
   Retrieved context is passed to **Llama 3.1 (via Groq)**  
   The model generates an answer with explicit source citations

---

## Backend Architecture

The backend is implemented using **FastAPI**, chosen for its performance and asynchronous capabilities.

### Key API Endpoints
- `POST /upload`  
  Handles PDF ingestion, chunking, embedding, and indexing
- `POST /chat`  
  Executes the RAG pipeline for question answering

---

## Frontend Interface

The frontend is built using **Streamlit**, providing a clean and intuitive user interface.

Users can:
- Upload research PDFs
- Ask questions in natural language
- View answers along with page-level citations

---

## Technology Stack

- Vector Database: Endee  
- LLM Inference: Groq (Llama-3.1-8b-instant)  
- Embeddings: sentence-transformers  
- Backend: FastAPI  
- Frontend: Streamlit  
- Language: Python 3.9+

---

## Setup and Execution Instructions

### Prerequisites
- Docker
- Python 3.9 or higher
- Git

---

### Step 1: Start Endee Vector Database

```bash
git clone https://github.com/EndeeLabs/endee
cd endee
```

Build and run the server (choose the correct CPU flag):

```bash
./install.sh --release --avx2
./run.sh
```

### Step 2: Configure Project Environment

Clone this repository and navigate to the project root directory.

Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

Install required dependencies:

```bash
pip install -r requirements.txt
```

### Step 3: Environment Variables

Create a `.env` file in the root directory and add the following configuration:

```
GROQ_API_KEY=your_groq_api_key_here
ENDEE_HOST=localhost
ENDEE_PORT=8080
```

### Step 4: Run the Application

Open two separate terminal windows.

**Terminal 1 – Start Backend API**

```bash
uvicorn backend.main:app --reload --port 8000
```

**Terminal 2 – Start Frontend UI**

```bash
streamlit run frontend/app.py
```

---

## Usage

1. Open the Streamlit application in your browser at `http://localhost:8501`

2. Upload an academic PDF document using the sidebar

3. Wait for the document to be processed and indexed

4. Enter a question in the chat interface

5. Receive an answer along with page-level source citations
