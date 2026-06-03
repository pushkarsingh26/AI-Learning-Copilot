import logging
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from src.config import settings
from src.vector_store import get_retriever

logger = logging.getLogger(__name__)

def get_llm() -> ChatOpenAI:
    """Initializes and returns the ChatOpenAI instance using OpenRouter."""
    return ChatOpenAI(
        model="google/gemma-3-27b-it",
        openai_api_key=settings.openrouter_api_key,
        openai_api_base="https://openrouter.ai/api/v1",
        temperature=0.3,
    )

def ask_question(question: str) -> Dict[str, Any]:
    """Uses RAG to answer a question based on uploaded context."""
    logger.info(f"Asking question: {question}")
    retriever = get_retriever()
    if not retriever:
        logger.warning("No FAISS index found. Cannot answer question.")
        return {"answer": "No index found. Please upload a document first.", "sources": []}
    
    docs = retriever.invoke(question)
    context = "\n\n".join(doc.page_content for doc in docs)
    sources = list(set([doc.metadata.get("source", "Unknown") for doc in docs]))
    
    prompt = f"""
    Answer the question based solely on the provided context.
    If you don't know the answer based on the context, say so.
    
    Context:
    {context}
    
    Question: {question}
    Answer:
    """
    
    try:
        llm = get_llm()
        response = llm.invoke(prompt)
        return {"answer": response.content.strip(), "sources": sources}
    except Exception as e:
        logger.error(f"Failed to fetch response from LLM: {e}")
        raise
