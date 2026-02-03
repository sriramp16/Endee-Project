import os
from groq import Groq
from typing import List, Dict

class RAGPipeline:
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)
        
    def generate_answer(self, query: str, context: List[Dict]) -> Dict:
        context_str = "\n\n".join([
            f"Source [{i+1}]: {item['text']} (File: {item['metadata'].get('filename')}, Page: {item['metadata'].get('page_number')})" 
            for i, item in enumerate(context)
        ])
        
        system_prompt = """You are an intelligent research assistant using RAG. 
Answer the user's question strictly based on the provided context. 
If the answer is not in the context, say "I cannot find the answer in the provided documents."
Cite your sources by referring to the Source numbers (e.g., [Source 1])."""

        user_prompt = f"""Context:\n{context_str}\n\nQuestion: {query}"""

        completion = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_completion_tokens=1024,
            top_p=1
        )
        
        answer = completion.choices[0].message.content
        
        return {
            "answer": answer,
            "citations": [c['metadata'] for c in context]
        }
