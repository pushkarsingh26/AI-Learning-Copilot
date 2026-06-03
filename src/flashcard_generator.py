import json
import re
from src.rag import get_llm
from src.vector_store import get_retriever

def generate_flashcards(topic: str):
    retriever = get_retriever()
    if not retriever:
        raise ValueError("No index found. Please upload a document first.")
        
    docs = retriever.invoke(topic)
    context = "\n\n".join(doc.page_content for doc in docs)
    
    prompt = f"""
    Using the context below,
    
    Generate 10 flashcards.
    
    Return ONLY JSON.
    
    Format example:
    [
      {{
        "front": "Term or question...",
        "back": "Definition or answer..."
      }}
    ]
    
    Context:
    {context}
    """
    
    llm = get_llm()
    response = llm.invoke(prompt)
    
    flashcards_json = response.content
    clean_json = re.sub(r"```json|```", "", flashcards_json).strip()
    
    try:
        flashcards = json.loads(clean_json)
        return flashcards
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse generated flashcards as JSON: {e}. Raw response: {clean_json}")
