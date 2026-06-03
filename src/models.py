from pydantic import BaseModel, Field
from typing import List, Optional

# Health Schema
class HealthResponse(BaseModel):
    status: str

# Upload PDF Schema
class UploadResponse(BaseModel):
    message: str
    chunks: int

# QA Schema
class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    answer: str
    sources: List[str]

# Quiz Schema
class QuizRequest(BaseModel):
    topic: str

class QuizOption(BaseModel):
    question: str
    options: List[str]
    answer: str

# Flashcard Schema
class FlashcardRequest(BaseModel):
    topic: str

class FlashcardResponse(BaseModel):
    front: str
    back: str

# Submit Quiz Schema
class SubmitQuizRequest(BaseModel):
    topic: str
    score: int
    total: int

# Progress Schema
class ProgressAttempt(BaseModel):
    topic: str
    score: int
    total: int
    created_at: str

class ProgressResponse(BaseModel):
    overall_accuracy: float
    attempts: List[ProgressAttempt]

# Weak Topics Schema
class WeakTopic(BaseModel):
    topic: str
    accuracy: float

# Adaptive Quiz Schema
class AdaptiveQuizResponse(BaseModel):
    topic: str
    quiz: List[QuizOption]
