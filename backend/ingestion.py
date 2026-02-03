import io
from pypdf import PdfReader
from typing import List, Dict

def extract_text_from_pdf(file_content: bytes, filename: str) -> List[Dict]:
    reader = PdfReader(io.BytesIO(file_content))
    pages_content = []
    
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            pages_content.append({
                "text": text,
                "page_number": i + 1,
                "filename": filename
            })
    return pages_content

def chunk_text(pages: List[Dict], chunk_size: int = 500, overlap: int = 50) -> List[Dict]:
    chunks = []
    chunk_id_counter = 0

    for page in pages:
        text = page["text"]
        
        start = 0
        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunk_text = text[start:end]
            
            chunks.append({
                "id": f"{page['filename']}_p{page['page_number']}_{chunk_id_counter}",
                "text": chunk_text,
                "metadata": {
                    "filename": page["filename"],
                    "page_number": page["page_number"],
                    "chunk_id": chunk_id_counter
                }
            })
            
            chunk_id_counter += 1
            start += (chunk_size - overlap)
            
    return chunks
