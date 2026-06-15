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

## 🚀 Getting Started

### Step 1: Install and Start Ollama
Ensure the Ollama application is running on your machine.
Open a terminal and pull the `llama3` model (the default model optimized for our strict RAG guardrails):
```bash
ollama pull llama3
```

### Step 2: Install Python Dependencies
Navigate to the `ai-service` directory and install the required packages:
```bash
cd ai-service
pip install -r requirements.txt
```

### Step 3: Start the Backend Server
Run the FastAPI backend using `uvicorn`:
```bash
python -m uvicorn api.main:app --host 127.0.0.1 --port 8080
```
*Note: On startup, the system will automatically parse the `data/` directory and build the ChromaDB vector embeddings.*

### Step 4: Access the Dashboard
The backend automatically serves the frontend interface. 
Simply open your web browser and navigate to:
👉 **http://127.0.0.1:8080/**

---

## 📂 Project Structure

```text
pineaple-rag/
├── ai-service/
│   ├── api/                  # FastAPI routes and server config
│   ├── data/                 # Simulated outputs from upstream microservices (.md)
│   ├── frontend/             # HTML/JS for the streaming chat interface
│   ├── ingestion/            # Logic for loading and semantic chunking of data
│   ├── rag/                  # RAG generator logic and ChromaDB client
│   ├── config.py             # Global configuration (Ports, Model Targets)
│   └── requirements.txt      # Python dependencies
└── .gitignore                # Excludes __pycache__ and massive vector db stores
```

---

## 🧪 Testing the AI
Try asking the AI questions that require it to cross-reference multiple layers of data. For example:
- *"What is wrong with Farm 1 Block C-3?"*
- *"Is the stress in Farm 2 Block W-2 caused by irrigation?"*
- *"Are there any missed operations we should be aware of?"*
