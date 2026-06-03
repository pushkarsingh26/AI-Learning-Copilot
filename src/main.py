import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import List, Dict, Any

from src.models import (
    HealthResponse,
    UploadResponse,
    AskRequest,
    AskResponse,
    QuizRequest,
    QuizOption,
    FlashcardRequest,
    FlashcardResponse,
    SubmitQuizRequest,
    ProgressResponse,
    WeakTopic,
    AdaptiveQuizResponse
)
from src.config import settings
from src.pdf_loader import load_and_split_pdf
from src.vector_store import save_to_vector_store
from src.rag import ask_question
from src.quiz_generator import generate_quiz
from src.flashcard_generator import generate_flashcards
from src.progress import submit_quiz_result, get_progress, get_weak_topics
from src.adaptive_learning import generate_adaptive_quiz

app = FastAPI(title="AI Learning Copilot")

@app.get("/health", response_model=HealthResponse)
def health_check():
    return {"status": "ok"}

@app.post("/upload-pdf", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
        
    file_path = os.path.join(settings.uploads_dir, file.filename)
    
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
        
    try:
        documents = load_and_split_pdf(file_path)
        if not documents:
            raise HTTPException(status_code=400, detail="No readable text found in PDF.")
            
        save_to_vector_store(documents)
        
        return {
            "message": "PDF processed successfully",
            "chunks": len(documents)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    try:
        result = ask_question(request.question)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-quiz", response_model=List[QuizOption])
def quiz(request: QuizRequest):
    try:
        quiz_data = generate_quiz(request.topic)
        return quiz_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-flashcards", response_model=List[FlashcardResponse])
def flashcards(request: FlashcardRequest):
    try:
        flashcards_data = generate_flashcards(request.topic)
        return flashcards_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/submit-quiz")
def submit_quiz(request: SubmitQuizRequest):
    try:
        result = submit_quiz_result(request.topic, request.score, request.total)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/progress", response_model=ProgressResponse)
def progress():
    try:
        return get_progress()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/weak-topics", response_model=List[WeakTopic])
def weak_topics():
    try:
        return get_weak_topics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/adaptive-quiz")
def adaptive_quiz():
    try:
        result = generate_adaptive_quiz()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
