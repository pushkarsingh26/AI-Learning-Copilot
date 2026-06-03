from src.database import get_db_connection

def submit_quiz_result(topic: str, score: int, total: int):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO quiz_results (topic, score, total)
            VALUES (?, ?, ?)
        """, (topic, score, total))
        conn.commit()
    finally:
        conn.close()
    return {"message": "Result Saved!"}

def get_progress():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        # Get overall accuracy
        cursor.execute("SELECT SUM(score), SUM(total) FROM quiz_results")
        correct, attempted = cursor.fetchone()
        
        accuracy = 0.0
        if attempted and attempted > 0:
            accuracy = (correct / attempted) * 100
            
        # Get individual attempts
        cursor.execute("SELECT * FROM quiz_results ORDER BY created_at DESC")
        rows = cursor.fetchall()
        attempts = [dict(row) for row in rows]
        
    finally:
        conn.close()
        
    return {
        "overall_accuracy": round(accuracy, 2),
        "attempts": attempts
    }

def get_weak_topics():
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
        """)
        rows = cursor.fetchall()
        
        WEAK_THRESHOLD = 70
        weak_topics = [{"topic": row["topic"], "accuracy": row["accuracy"]} for row in rows if row["accuracy"] < WEAK_THRESHOLD]
        
    finally:
        conn.close()
        
    return weak_topics
