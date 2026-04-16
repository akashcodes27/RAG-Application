"""
PDF Agent — handles unstructured document Q&A using FAISS + HuggingFace embeddings + Ollama
"""

import os
from PyPDF2 import PdfReader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from google import genai
from langchain_ollama import ChatOllama


# ── PDF Processing ────────────────────────────────────────────────────────────

def get_pdf_text(pdf_docs) -> str:
    text = ""
    for pdf in pdf_docs:
        reader = PdfReader(pdf)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted
    return text


def get_text_chunks(text: str) -> list:
    splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    return splitter.split_text(text)


def get_vectorstore(text_chunks: list):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    return FAISS.from_texts(texts=text_chunks, embedding=embeddings)


def get_retriever(vectorstore):
    return vectorstore.as_retriever(search_kwargs={"k": 4})


# ─────────────────────────────────────────────────────────────────

def ask_pdf_question(user_question: str, retriever) -> str:
    docs = retriever.invoke(user_question)
    context = "\n\n".join([doc.page_content for doc in docs])

    llm = ChatOllama(model="llama3.2", temperature=0)

    prompt = f"""You are a helpful assistant for answering questions about uploaded PDF documents.
Use only the provided context to answer the question.
If the answer is not present in the context, say: "I could not find that information in the uploaded documents."

Context:
{context}

Question:
{user_question}

Answer:"""

    response = llm.invoke(prompt)
    return response.content
