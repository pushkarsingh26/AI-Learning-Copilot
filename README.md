# AI Learning Copilot

AI Learning Copilot is a powerful backend API and Streamlit application for analyzing reading materials via an intelligent pipeline (RAG) and dynamically creating targeted micro-learning outputs (quizzes, flashcards) to streamline and optimize learning routines. 

## Features
- **PDF Upload and Indexing:** Automatically extracts text, chunks it, and creates FAISS embeddings.
- **RAG QA:** Ask the model questions directly using context parsed from uploaded material.
- **Micro-Learning:** Generates dynamic 5-question Multi-Choice quizzes or flashcard banks based on user topics.
- **Progress & Tracking:** Tracks your overall progress based on submitted outcomes via SQLite.
- **Adaptive Modules:** Scans existing DB records to detect weak points and automatically queues remedial tests focused entirely on failing topics.

## Environment Setup
1. Define your environment parameters either in an environment variable or via a newly created `.env` file (you can view the `.env.example` file for standard variables):

```env
OPENROUTER_API_KEY=your_actual_key_here
DATA_DIR=data
```

## Installation
Make sure you have python `>3.11` installed.
Navigate to the directory containing `pyproject.toml` or `requirements.txt`.

Install dependencies leveraging `uv`:
```bash
uv pip install -r requirements.txt
```
Or directly:
```bash
pip install -r requirements.txt
```

## Running the API (Backend)
Run the uvicorn server passing your app pointer natively:
```bash
uvicorn src.main:app --reload
```
You can access Interactive OpenAPI Documentation at: `http://127.0.0.1:8000/docs`.

### Simple Health Check test
```bash
curl http://localhost:8000/health
```

## Running the Streamlit App (Frontend)
Make sure the backend is active on PORT 8000. Open a new terminal and run:
```bash
streamlit run streamlit_app.py
```
This spawns a dynamic interface where you can experiment directly with the services.

## Project Architecture
- `src/main.py`: Core FastAPI routing paths.
- `src/config.py`: Environment variable and schema loader relying on Pydantic.
- `src/database.py`: Core SQLite generation schema processing connection parameters.
- `src/models.py`: Static Pydantic configurations defining inputs/outputs for Type Hinting formatting.
- `src/pdf_loader.py` & `src/vector_store.py` & `src/embeddings.py`: The document ingestion -> storage pipeline using PyMuPDF and FAISS models (SentenceTransformers).
- `src/quiz_generator.py` & `src/flashcard_generator.py`: Specific module integrations prompting strictly valid JSON configurations for the UI parser logic via OpenRouter (Gemma).
- `src/adaptive_learning.py` & `src/progress.py`: Generative analysis comparing retrieved analytics records natively on DB files. 
