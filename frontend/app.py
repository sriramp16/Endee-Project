import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = "http://localhost:8000"

st.set_page_config(page_title="RAG Research Assistant", layout="wide")

st.title("Intelligent Research Assistant")
st.markdown(f"Powered by **Endee Vector Database** & **Groq**")

with st.sidebar:
    st.header("Document Upload")
    uploaded_file = st.file_uploader("Upload a Research Paper (PDF)", type=["pdf"])
    
    if uploaded_file and st.button("Process Document"):
        with st.spinner("Processing..."):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
            try:
                response = requests.post(f"{API_URL}/upload", files=files)
                if response.status_code == 200:
                    st.success(response.json()["message"])
                else:
                    st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"Connection failed: {e}")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question about your documents..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Generating answer..."):
            try:
                payload = {"message": prompt, "history": []} 
                response = requests.post(f"{API_URL}/chat", json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    answer = data["answer"]
                    st.markdown(answer)
                    
                    with st.expander("View Sources"):
                        for i, citation in enumerate(data.get("citations", [])):
                            st.markdown(f"**Source {i+1}**: {citation.get('filename')} (Page {citation.get('page_number')})")
                    
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error(f"Backend Error: {response.text}")
            except Exception as e:
                st.error(f"Failed to connect to backend: {e}")
