# Intelligent Research Assistant using RAG and Endee Vector Database

This project is a production-ready Intelligent Research Assistant designed to help researchers and students efficiently interact with academic papers. By leveraging **Retrieval Augmented Generation (RAG)**, the system answers user queries with precise citations, grounded strictly in the provided document context.

The core of this application is built on the **Endee Vector Database**, utilizing its high-performance C++ backend for low-latency vector search and retrieval.

## Problem Statement
Researchers often struggle to find specific information within lengthy academic PDFs. Standard keyword search is insufficient for understanding context. This project solves that problem by implementing:
1.  **Semantic Search**: Understanding the meaning behind a query rather than just matching keywords.
2.  **Generative Answers**: synthesizing retrieved information into a coherent answer.
3.  **Source Attribution**: Providing page-level citations to build trust in the AI's output.

## Architecture & Technical Approach

### 1. Vector Database: Endee
We use **Endee** (https://github.com/EndeeLabs/endee) as the dedicated vector store. Endee was chosen for its:
*   **Performance**: Highly optimized C++ core for fast nearest-neighbor search.
*   **Scalability**: Efficient management of high-dimensional embeddings.
*   **Simplicity**: Clean API structure for vector insertion and retrieval.

### 2. Retrieval Augmented Generation (RAG) Pipeline
The system follows a standard RAG workflow:
1.  **Ingestion**: PDFs are uploaded, text is extracted, and split into overlapping chunks (size: 500 chars, overlap: 50).
2.  **Embedding**: Chunks are converted into 384-dimensional vectors using `sentence-transformers/all-MiniLM-L6-v2`.
3.  **Storage**: Vectors and metadata (filename, page number) are indexed in Endee.
4.  **Retrieval**: User queries are converted to vectors, and Endee performs a similarity search to find the top 5 most relevant chunks.
5.  **Generation**: The retrieved context is passed to Groq (Llama 3.1), which generates an answer citing the specific sources.

### 3. Backend (FastAPI)
The backend is built with **FastAPI** for asynchronous performance. Key endpoints:
*   `POST /upload`: Handles PDF processing and vector indexing.
*   `POST /chat`: Manages the RAG inference loop.

### 4. Frontend (Streamlit)
A clean, responsive user interface built with **Streamlit** allows users to upload documents and chat with the assistant in real-time.

## Technology Stack
*   **Vector Database**: Endee
*   **LLM Inference**: Groq (Llama-3.1-8b-instant)
*   **Embeddings**: sentence-transformers
*   **Backend Framework**: FastAPI
*   **Frontend Framework**: Streamlit
*   **Language**: Python 3.9+

## Setup and Execution Instructions

### Prerequisites
*   Docker (for running Endee)
*   Python 3.9 or higher
*   Git

### Step 1: Start Endee Vector Database
Endee must be running as a service.
1.  Clone the Endee repository:
    ```bash
    git clone https://github.com/EndeeLabs/endee
    cd endee
    ```
2.  Build and run the server (ensure you select the flag matching your CPU, e.g., --avx2):
    ```bash
    ./install.sh --release --avx2
    ./run.sh
    ```

### Step 2: Configure Project Environment
1.  Clone this repository and navigate to the root directory.
2.  Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Step 3: Environment Variables
Create a file named `.env` in the root directory and add your configurations:
```
GROQ_API_KEY=your_groq_api_key_here
ENDEE_HOST=localhost
ENDEE_PORT=8080
```

### Step 4: Run the Application
Open two separate terminal windows.

**Terminal 1: Start Backend API**
```bash
uvicorn backend.main:app --reload --port 8000
```

**Terminal 2: Start Frontend UI**
```bash
streamlit run frontend/app.py
```

## Usage
1.  Open your browser to the Streamlit local URL (default: `http://localhost:8501`).
2.  Use the sidebar to upload a PDF research paper.
3.  Wait for the processing confirmation.
4.  Enter your question in the chat input. The system will respond with an answer and list the source pages used.
