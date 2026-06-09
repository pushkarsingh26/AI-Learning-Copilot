<div align="center">

<img src="./assets/banner.png" alt="AI Learning Copilot Banner" width="100%"/>

<br/>

# 🎓 AI Learning Copilot

**Your intelligent study partner — powered by RAG, LLMs, and adaptive micro-learning.**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.136+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.58+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![LangChain](https://img.shields.io/badge/LangChain-1.3+-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://langchain.com)
[![OpenRouter](https://img.shields.io/badge/OpenRouter-Gemma_3_27B-6C63FF?style=for-the-badge&logo=google&logoColor=white)](https://openrouter.ai)
[![FAISS](https://img.shields.io/badge/FAISS-Vector_Search-00BFFF?style=for-the-badge&logo=meta&logoColor=white)](https://github.com/facebookresearch/faiss)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](LICENSE)
[![Live Demo](https://img.shields.io/badge/Live_Demo-Streamlit_Cloud-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://ai-learning-copilot-vknhansxzzrccw6prweg6s.streamlit.app/)

<br/>

> Upload any PDF → Ask questions → Generate quizzes & flashcards → Track your progress → Let AI adapt to your weaknesses.

<br/>

[🌐 Live Demo](https://ai-learning-copilot-vknhansxzzrccw6prweg6s.streamlit.app/) • [🚀 Quick Start](#-quick-start) • [✨ Features](#-features) • [🏗️ Architecture](#️-architecture) • [📡 API Reference](#-api-reference) • [🖥️ Screenshots](#️-app-pages) • [🤝 Contributing](#-contributing)

</div>

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 📄 PDF Upload & Indexing
Upload any PDF learning material. The system automatically extracts text, chunks it intelligently, and creates **FAISS vector embeddings** using SentenceTransformers — ready for instant semantic search.

</td>
<td width="50%">

### 💬 RAG-Powered Q&A
Ask natural language questions directly from your uploaded documents. A **Retrieval-Augmented Generation (RAG)** pipeline fetches the most relevant chunks and passes them to Google Gemma 3 27B via OpenRouter for grounded, context-aware answers.

</td>
</tr>
<tr>
<td width="50%">

### 📝 Dynamic Quiz Generation
Generate **5-question multiple-choice quizzes** on any topic in seconds. Questions are AI-generated with distractors and correct answers, rendered in an interactive form with real-time scoring and answer review.

</td>
<td width="50%">

### 🗂️ Flashcard Generator
Create **spaced-repetition-style flashcards** for any topic. Each card has a front (question/term) and back (answer/definition), displayed in a collapsible card deck for quick revision sessions.

</td>
</tr>
<tr>
<td width="50%">

### 📈 Progress Tracking
Every quiz attempt is persisted in **SQLite** with timestamps. The Progress page visualises your accuracy trend over time (line chart) and performance per topic (bar chart), powered by Plotly.

</td>
<td width="50%">

### 🧠 Adaptive Learning
The AI analyses your historical quiz data to **detect your weakest topic** and automatically generates a targeted remedial quiz — so you always focus where it matters most.

</td>
</tr>
</table>

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                        Streamlit Frontend                        │
│   Dashboard │ Upload │ Q&A │ Quiz │ Flashcards │ Progress │ Adaptive │
└─────────────────────────┬────────────────────────────────────────┘
                          │ HTTP (REST)
┌─────────────────────────▼────────────────────────────────────────┐
│                    FastAPI Backend (uvicorn)                      │
│  /health  /upload-pdf  /ask  /generate-quiz  /generate-flashcards│
│  /submit-quiz  /progress  /weak-topics  /adaptive-quiz           │
└────┬──────────────┬──────────────┬─────────────────┬─────────────┘
     │              │              │                 │
┌────▼────┐  ┌──────▼──────┐  ┌───▼───┐  ┌──────────▼─────────┐
│  PyMuPDF│  │SentenceXfmrs│  │OpenRtr│  │    SQLite + SQLAlch │
│PDF Load │  │  + FAISS    │  │Gemma3 │  │  Progress & History │
│& Chunker│  │Vector Store │  │  LLM  │  │                    │
└─────────┘  └─────────────┘  └───────┘  └────────────────────┘
```

### Module Map

| File | Responsibility |
|------|---------------|
| `src/main.py` | FastAPI app — all route definitions |
| `src/config.py` | Pydantic Settings — env variable loading |
| `src/models.py` | Request/Response Pydantic schemas |
| `src/pdf_loader.py` | PyMuPDF text extraction + LangChain text splitting |
| `src/embeddings.py` | SentenceTransformers embedding model initialisation |
| `src/vector_store.py` | FAISS index build, save, load, and retriever factory |
| `src/rag.py` | RAG pipeline — retrieval → prompt → OpenRouter LLM → answer |
| `src/quiz_generator.py` | LLM prompt engineering for JSON quiz output |
| `src/flashcard_generator.py` | LLM prompt engineering for JSON flashcard output |
| `src/database.py` | SQLite schema setup via SQLAlchemy |
| `src/progress.py` | Quiz result persistence, overall accuracy, weak topic detection |
| `src/adaptive_learning.py` | Adaptive quiz logic — weakest topic → targeted quiz |
| `streamlit_app.py` | Full 8-page Streamlit frontend |

---

## 🚀 Quick Start

### Prerequisites

- Python **≥ 3.11**
- An **[OpenRouter](https://openrouter.ai)** API key (free tier works)

### 1 · Clone the Repository

```bash
git clone https://github.com/pushkarsingh26/AI-Learning-Copilot.git
cd AI-Learning-Copilot
```

### 2 · Configure Environment

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
DATA_DIR=data
```

> 💡 Get a free API key at [openrouter.ai/keys](https://openrouter.ai/keys). The app uses **Google Gemma 3 27B** which is available on the free tier.

### 3 · Install Dependencies

**Option A — Using `uv` (recommended, fast):**

```bash
pip install uv
uv pip install -r requirements.txt
```

**Option B — Using standard pip:**

```bash
pip install -r requirements.txt
```

### 4 · Run the Backend API

```bash
uvicorn src.main:app --reload --port 8080
```

The FastAPI server starts at **`http://127.0.0.1:8080`**
Interactive API docs available at **`http://127.0.0.1:8080/docs`**

### 5 · Run the Streamlit Frontend

Open a **new terminal** (keep the backend running) and execute:

```bash
streamlit run streamlit_app.py
```

Your browser will automatically open the Copilot UI. 🎉

---

## 📡 API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Backend health check |
| `POST` | `/upload-pdf` | Upload & index a PDF file |
| `POST` | `/ask` | Ask a question via RAG |
| `POST` | `/generate-quiz` | Generate a 5-question MCQ quiz |
| `POST` | `/generate-flashcards` | Generate a flashcard set |
| `POST` | `/submit-quiz` | Record a quiz score to SQLite |
| `GET` | `/progress` | Fetch overall accuracy & attempt history |
| `GET` | `/weak-topics` | List topics with accuracy below 70% |
| `GET` | `/adaptive-quiz` | Auto-generate a quiz for your weakest topic |

### Example Requests

**Ask a question (RAG):**
```bash
curl -X POST http://localhost:8080/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the main idea of chapter 3?"}'
```

**Generate a quiz:**
```bash
curl -X POST http://localhost:8080/generate-quiz \
  -H "Content-Type: application/json" \
  -d '{"topic": "Photosynthesis"}'
```

**Upload a PDF:**
```bash
curl -X POST http://localhost:8080/upload-pdf \
  -F "file=@/path/to/your/document.pdf"
```

---

## 🖥️ App Pages

| Page | Description |
|------|-------------|
| 📊 **Dashboard** | API status, total quiz attempts, overall accuracy, weak topic alerts |
| 📄 **Upload PDF** | Drag-and-drop PDF uploader with chunk count feedback |
| 💬 **Ask Questions** | RAG-powered Q&A with source document references |
| 📝 **Generate Quiz** | Topic-based MCQ quiz with interactive form and score review |
| 🗂️ **Flashcards** | Collapsible flashcard deck for spaced repetition |
| 📈 **Progress Tracking** | Accuracy trend line chart + per-topic bar chart (Plotly) |
| 🔍 **Weak Topics** | Visual progress bars for topics below 70% accuracy |
| 🧠 **Adaptive Learning** | One-click adaptive quiz targeting your worst-performing topic |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Streamlit 1.58+, Plotly, Pandas |
| **Backend** | FastAPI 0.136+, Uvicorn, Pydantic v2 |
| **LLM** | Google Gemma 3 27B via OpenRouter (LangChain-OpenAI) |
| **Embeddings** | SentenceTransformers (`all-MiniLM-L6-v2`) |
| **Vector Store** | FAISS (CPU) |
| **PDF Processing** | PyMuPDF + LangChain Text Splitters |
| **Database** | SQLite via SQLAlchemy 2.0 |
| **LLM Orchestration** | LangChain 1.3, LangGraph 1.2 |
| **Config** | Pydantic-Settings, python-dotenv |
| **Notebooks** | JupyterLab (RAG pipeline & quiz prototyping) |

---

## 📁 Project Structure

```
AI-Learning-Copilot/
├── 📂 assets/               # Static assets (banner, screenshots)
├── 📂 data/                 # Uploaded PDFs & FAISS index storage
├── 📂 notebooks/            # Jupyter notebooks for prototyping
│   ├── rag_pipeline.ipynb
│   └── quiz_flashcards.ipynb
├── 📂 src/                  # Core application modules
│   ├── main.py              # FastAPI routes
│   ├── config.py            # Environment config
│   ├── models.py            # Pydantic schemas
│   ├── database.py          # SQLite setup
│   ├── pdf_loader.py        # PDF text extraction
│   ├── embeddings.py        # Embedding model
│   ├── vector_store.py      # FAISS operations
│   ├── rag.py               # RAG Q&A pipeline
│   ├── quiz_generator.py    # Quiz generation
│   ├── flashcard_generator.py # Flashcard generation
│   ├── progress.py          # Progress tracking
│   └── adaptive_learning.py # Adaptive quiz logic
├── streamlit_app.py         # Streamlit frontend (8 pages)
├── pyproject.toml           # Project metadata & dependencies
├── requirements.txt         # Pinned dependency list
├── .env                     # Local environment variables (git-ignored)
└── .gitignore
```

---

## 🔧 Configuration

All settings are managed via environment variables (loaded through Pydantic Settings):

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENROUTER_API_KEY` | — | **Required.** Your OpenRouter API key |
| `DATA_DIR` | `data` | Directory for uploaded PDFs & FAISS index |

---

## 🧪 Development

### Running Notebooks

The `notebooks/` directory contains exploratory Jupyter notebooks for prototyping the RAG pipeline and quiz/flashcard generators:

```bash
jupyter lab notebooks/
```

### Health Check

```bash
curl http://localhost:8080/health
# → {"status": "ok"}
```

### Interactive API Docs

Once the backend is running, visit:
- **Swagger UI**: `http://127.0.0.1:8080/docs`
- **ReDoc**: `http://127.0.0.1:8080/redoc`

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m 'feat: add amazing feature'`
4. **Push** to your branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

---

## 👤 Author

**Pushkar Chhokar**
- 🐙 [@pushkarsingh26](https://github.com/pushkarsingh26)

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

Made with ❤️ and a lot of ☕ by **Pushkar Chhokar**

⭐ Star this repo if you find it useful!

</div>
