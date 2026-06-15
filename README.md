# Agritech AI RAG System 🍍

A dynamic, self-hosted, Retrieval-Augmented Generation (RAG) system built to act as the central "brain" for an Agritech platform. 

This project simulates a downstream AI Analysis Service that consumes tabular output from various microservices (Plant Detection, Vegetation Index, IoT Sensors, and Operations) and uses a local Large Language Model to provide actionable, cross-functional agronomic insights to estate managers.

## 🌟 Features
- **Local Privacy**: Runs 100% locally using Ollama. No farm data leaves your server.
- **Dynamic Streaming**: The frontend chat interface dynamically streams responses token-by-token (Server-Sent Events) for a fast, commercial-grade UX.
- **Strict Guardrails**: Implements severe negative constraints to prevent LLM hallucinations and cross-farm data contamination.
- **Semantic Markdown Chunking**: Custom chunking logic ensures that simulated CSV/tabular data (rendered as Markdown) is not broken apart, preserving exact plant ID and location matching.

---

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed:
1. **Python 3.10+**: Download from [python.org](https://www.python.org/downloads/).
2. **Ollama**: Download from [ollama.com](https://ollama.com/).

---

## 🐳 Docker Deployment (Recommended)

The easiest way to run the entire system is using Docker. This fully automates the backend server and pulls the required AI models automatically.

```bash
docker-compose up --build -d
```
Wait a few minutes for the system to start (it will download the `llama3` model in the background on its first run). 
Then, open your browser and navigate to:
👉 **http://127.0.0.1:8080/**

---

## 🚀 Manual Local Setup

---

### Step 1: Download the AI Model
Open a terminal and run this once to download the `llama3` model (~4.7 GB):
```bash
ollama pull llama3
```
Wait for the download to finish before continuing.

---

### Step 2: Keep Ollama Running (Terminal 1 — leave this open)
**This is the step most people miss.** Ollama must be actively running as a background service for the AI to work. In your **first terminal**, run:
```bash
ollama serve
```
You should see output like `Listening on 127.0.0.1:11434`. **Leave this terminal open.** If you close it, the AI will stop working.

---

### Step 3: Install Python Dependencies (Terminal 2)
Open a **second terminal**, navigate to the `ai-service` directory, and install packages:
```bash
cd ai-service
pip install -r requirements.txt
```

---

### Step 4: Start the Backend Server (Terminal 2)
In the same second terminal, run:
```bash
python -m uvicorn api.main:app --host 127.0.0.1 --port 8080
```
On startup, the system will automatically parse the `data/` directory and build the ChromaDB vector index. You'll see `Successfully indexed X chunks.` when it's ready.

---

### Step 5: Access the Dashboard
Open your web browser and navigate to:
👉 **http://127.0.0.1:8080/**

---

## 🔧 Troubleshooting

### "Error calling Ollama: All connection attempts failed"
This means Ollama is **not running**. Go back to Step 2 and make sure `ollama serve` is running in a separate terminal window.

### "Error calling Ollama: ..." (other errors)
- Make sure you have pulled the model first: `ollama pull llama3`
- Confirm Ollama is listening on port `11434` by visiting `http://127.0.0.1:11434` in your browser — you should see `Ollama is running`.

### ChromaDB / embedding errors on startup
Delete the `ai-service/chroma_store/` folder and restart the backend. It will rebuild the index automatically.

---

## 📂 Project Structure

```text
pineaple-rag/
├── ai-service/
│   ├── api/                  # FastAPI routes and server config
│   ├── data/                 # Knowledge base (.md files fed into the RAG pipeline)
│   ├── frontend/             # Streaming chat UI (HTML/JS)
│   ├── ingestion/            # Semantic chunking and data loading logic
│   ├── rag/                  # Generator and ChromaDB retriever
│   ├── config.py             # Global config (ports, model targets)
│   └── requirements.txt      # Python dependencies
└── .gitignore
```

---

## 🧪 Testing the AI
Try asking the AI questions that require it to cross-reference multiple layers of data. For example:
- *"What is wrong with Farm 1 Block C-3?"*
- *"Is the stress in Farm 2 Block W-2 caused by irrigation?"*
- *"Are there any missed operations we should be aware of?"*
