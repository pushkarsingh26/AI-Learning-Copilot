import json
import re
from src.rag import get_llm
from src.vector_store import get_retriever

def generate_quiz(topic: str, context: str = None):
    if not context:
        retriever = get_retriever()
        if not retriever:
            raise ValueError("No index found and no context provided. Please upload a document first.")
            
        docs = retriever.invoke(topic)
        context = "\n\n".join(doc.page_content for doc in docs)
    
    prompt = f"""
    You are a quiz generator.
    
    Generate 5 MCQs from the context.
    
    IMPORTANT:
    - Return ONLY valid JSON.
    - Do NOT use markdown.
    - Do NOT wrap output in ```json.
    - Do NOT add explanations.
    - Output must start with [ and end with ].
    
    Format example:
    [
      {{
        "question": "What is...?",
        "options": ["A", "B", "C", "D"],
        "answer": "A"
      }}
    ]
    
    Context:
    {context}
    """
    
    llm = get_llm()
    response = llm.invoke(prompt)
    
    quiz_json = response.content
    clean_json = re.sub(r"```json|```", "", quiz_json).strip()
    
    try:
        quiz = json.loads(clean_json)
        return quiz
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse generated quiz as JSON: {e}. Raw response: {clean_json}")
