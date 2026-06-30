# 📄 Intelligent Document Research Assistant

An AI-powered document research tool that lets you upload PDFs and ask natural-language questions about their content. Built with **RAG (Retrieval-Augmented Generation)** using LangChain, ChromaDB, and Groq's Llama 3.1 LLM.

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![React](https://img.shields.io/badge/React-19-61DAFB?logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi)
![LangChain](https://img.shields.io/badge/LangChain-RAG-green)
![Groq](https://img.shields.io/badge/Groq-Llama_3.1-orange)

---

## ✨ Features

- **📤 PDF Upload** — Upload one or multiple PDF documents via the UI
- **🔍 Semantic Search** — Chunks documents and creates vector embeddings for intelligent retrieval
- **🤖 AI-Powered Q&A** — Ask natural-language questions and get answers grounded in your documents
- **📑 Source Attribution** — See which document sections were used to generate each answer
- **⚡ Fast Inference** — Powered by Groq's Llama 3.1 8B Instant for near real-time responses
- **🎨 Two UI Modes** — Use the Streamlit standalone app or the full-stack React + FastAPI interface

---

## 🏗️ Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│  React UI   │────▶│  FastAPI API  │────▶│  LangChain RAG  │
│  (Vite +TS) │     │  (Backend)   │     │    Pipeline      │
└─────────────┘     └──────────────┘     └────────┬────────┘
                                                   │
                          ┌────────────────────────┼────────────────────┐
                          ▼                        ▼                    ▼
                   ┌─────────────┐       ┌──────────────┐    ┌─────────────────┐
                   │  ChromaDB   │       │  HuggingFace │    │   Groq API      │
                   │ Vector Store│       │  Embeddings  │    │  (Llama 3.1)    │
                   └─────────────┘       └──────────────┘    └─────────────────┘
```

---

## 📁 Project Structure

```
├── app.py                  # Streamlit standalone web app
├── build_index.py          # CLI script to build vector index
├── test_query.py           # CLI script to test Q&A
├── rag_basic.py            # Early RAG prototype
├── requirements.txt        # Python dependencies
│
├── src/                    # Core Python modules
│   ├── config.py           # Configuration (API keys, model names, paths)
│   ├── ingest.py           # PDF loading, chunking, vector store management
│   └── rag.py              # Question answering logic
│
├── backend/                # FastAPI REST API server
│   └── main.py             # API endpoints (upload, rebuild-index, ask)
│
└── frontend/               # React + TypeScript + Vite frontend
    ├── package.json
    ├── vite.config.ts
    └── src/
        ├── App.tsx          # Main React component
        └── main.tsx         # React entry point
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- Node.js & npm
- A [Groq API key](https://console.groq.com/)

### 1. Clone the Repository

```bash
git clone https://github.com/Rishikesh26022006/rag-document-assistant.git
cd rag-document-assistant
```

### 2. Backend Setup

```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux

# Install dependencies
pip install -r requirements.txt
pip install fastapi uvicorn    # For full-stack mode
```

### 3. Configure Environment

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Add Your Documents

Place your PDF files in the `data/` directory.

---

## ▶️ Running the App

### Option A: Streamlit (Standalone — Quickest)

```bash
streamlit run app.py
```

Opens at `http://localhost:8501` with upload sidebar and Q&A interface.

### Option B: Full-Stack (React + FastAPI)

**Start the backend:**

```bash
uvicorn backend.main:app --reload --port 8000
```

**Start the frontend:**

```bash
cd frontend
npm install
npm run dev
```

The React app connects to the API at `http://localhost:8000`.

### CLI Tools

```bash
python build_index.py     # Build vector index from PDFs in data/
python test_query.py      # Test Q&A from the terminal
```

---

## 🔌 API Endpoints

| Method | Endpoint          | Description               |
|--------|-------------------|---------------------------|
| GET    | `/`               | Health check              |
| GET    | `/documents`      | List uploaded documents   |
| POST   | `/upload`         | Upload a PDF file         |
| POST   | `/rebuild-index`  | Rebuild the vector index  |
| POST   | `/ask`            | Ask a question            |

---

## 🛠️ Tech Stack

| Layer       | Technology                                      |
|-------------|--------------------------------------------------|
| **LLM**     | Groq API — Llama 3.1 8B Instant                 |
| **Embeddings** | HuggingFace `all-MiniLM-L6-v2`               |
| **Vector DB** | ChromaDB                                       |
| **RAG Framework** | LangChain                                  |
| **Backend** | FastAPI + Uvicorn                                |
| **Frontend** | React 19 + TypeScript + Vite + Tailwind CSS    |
| **Standalone UI** | Streamlit                                   |

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<p align="center">
  Built with ❤️ by <a href="https://github.com/Rishikesh26022006">Rishikesh Sonawane</a>
</p>
