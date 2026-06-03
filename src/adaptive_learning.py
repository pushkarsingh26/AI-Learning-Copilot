from src.database import get_db_connection
from src.vector_store import get_retriever
from src.quiz_generator import generate_quiz

def generate_adaptive_quiz():
    # Find weakest topic
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                topic, 
                ROUND((SUM(score) * 100.0) / SUM(total), 2) as accuracy 
            FROM quiz_results 
            GROUP BY topic 
            ORDER BY accuracy ASC 
            LIMIT 1
        """)
        result = cursor.fetchone()
    finally:
        conn.close()
        
    if not result:
        return {"message": "No past quiz data available to generate adaptive quiz. Take a quiz first!"}
        
    weakest_topic = result["topic"]
    
    # Retrieve relevant chunks
    retriever = get_retriever()
    if not retriever:
        raise ValueError("No index found. Please upload a document first.")
        
    docs = retriever.invoke(weakest_topic)
    context = "\n\n".join(doc.page_content for doc in docs)
    
    # Generate quiz using the specific context for the weak topic
    quiz = generate_quiz(weakest_topic, context=context)
    
    return {
        "topic": weakest_topic,
        "quiz": quiz
    }
