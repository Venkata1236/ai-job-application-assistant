"""
rag_pipeline.py
Builds a FAISS retriever by indexing the CV and
job description using OpenAI embeddings.
"""
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


def build_retriever(jd_text: str, cv_text: str):
    """
    Build a FAISS retriever from job description and CV text.
    Returns top-4 relevant chunks on query.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    docs = splitter.create_documents(
        [jd_text, cv_text],
        metadatas=[
            {"source": "job_description"},
            {"source": "cv"}
        ]
    )

    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)

    return vectorstore.as_retriever(search_kwargs={"k": 4})