# Agritech AI Service — Complete Handoff & Continuation Prompt
## For: Gemini Pro | Role: Lead Developer taking this to production-ready

---

## WHO ARE YOU AND WHAT IS THIS PROJECT?

You are continuing development of the **Agritech AI Analysis Service** — a RAG-based AI chat assistant embedded in a plantation farm management platform. The system manages three farms (pineapple and oil palm estates in Malaysia). The AI assistant answers questions about farm health, vegetation indices, alerts, and workforce, and generates daily intelligence briefs.

The backend is a **FastAPI Python microservice** using:
- **ChromaDB** (local persistent vector store)
- **Ollama** (self-hosted LLM, variable model selection — user picks llama3, mistral, gemma2, etc.)
- **APScheduler** for the daily 06:00 intelligence brief

The frontend is a **standalone dark-themed HTML page** served directly by the FastAPI app at `/`.

A previous developer has built the entire codebase skeleton. The UI is confirmed working (screenshot verified). The issue is the app cannot connect to Ollama because it was built pointing at a Docker hostname (`ollama`) while the developer ran it bare-Python locally. Your job is to fix all known bugs, wire Ollama up correctly, and get the full chat pipeline working end-to-end.

---

## CURRENT STATE OF THE CODEBASE

### Project root: `c:\pineaple-rag\`

```
c:\pineaple-rag\
+-- docker-compose.yml               <- Production deployment config (working, unused for now)
+-- PROJECT_SPEC.md                  <- Full original project specification (reference doc)
+-- knowledge_base.md                <- Scraped farm dashboard data (source doc)
+-- rag_system_prompt.md             <- Agronomic inference rules (source doc)
|
+-- ai-service\                      <- THE MICROSERVICE
    +-- Dockerfile                   <- Working
    +-- requirements.txt             <- All deps installed
    +-- config.py                    <- BUG: wrong default Ollama URL
    |
    +-- api\
    |   +-- __init__.py
    |   +-- main.py                  <- BUG: asyncio.create_task misuse
    |   +-- models.py                <- Working
    |   +-- auth.py                  <- INCOMPLETE: needs dev bypass mode
    |
    +-- ingestion\
    |   +-- __init__.py
    |   +-- chunker.py               <- Working but needs verification
    |   +-- loader.py                <- Module-level ChromaDB init causes import crash
    |
    +-- rag\
    |   +-- __init__.py
    |   +-- retriever.py             <- Module-level ChromaDB init causes import crash
    |   +-- generator.py             <- BUG: Ollama URL is wrong (Docker hostname)
    |   +-- daily_brief.py           <- Working
    |
    +-- data\
    |   +-- knowledge_base.md        <- Present (copied from root)
    |   +-- rag_system_prompt.md     <- Present (copied from root)
    |
    +-- frontend\
    |   +-- index.html               <- Working UI (dark theme, model selector, severity badges)
    |
    +-- chroma_store\                <- ChromaDB creates this automatically
```

### Python environment
- Python 3.12 is installed and on PATH.
- All packages from `requirements.txt` are already installed globally.
- Server is run with: `python -m uvicorn api.main:app --host 127.0.0.1 --port 8080` from inside `c:\pineaple-rag\ai-service\`

---

## KNOWN BUGS — FULL LIST

### BUG 1 — Wrong Ollama default URL (CRITICAL)
**File**: `config.py` line 3
**Problem**: Default URL is `http://ollama:11434`. This is a Docker internal hostname. When running bare-Python locally, Ollama is at `http://localhost:11434`, causing `[Errno 11001] getaddrinfo failed` — which is the error visible in the chat screenshot.
**Fix**: Change default to `http://localhost:11434`. In `docker-compose.yml`, override via env var `OLLAMA_BASE_URL=http://ollama:11434`.

### BUG 2 — asyncio.create_task() in lifespan (MEDIUM)
**File**: `api/main.py` line 33
**Problem**: `asyncio.create_task(generate_daily_brief())` is not safe inside an asynccontextmanager lifespan handler. Can raise RuntimeError or silently fail.
**Fix**: Use APScheduler to schedule a one-time `date` trigger 10 seconds after startup instead:
  `scheduler.add_job(generate_daily_brief, 'date', run_date=datetime.now() + timedelta(seconds=10))`

### BUG 3 — Module-level ChromaDB client init (MEDIUM)
**Files**: `ingestion/loader.py` lines 8-11, `rag/retriever.py` lines 4-6
**Problem**: Two separate chromadb.PersistentClient instances at module level — potential SQLite write conflicts, and relative path resolution depends on CWD at import time.
**Fix**: Create a new file `rag/chroma_client.py` with a singleton lazy-init pattern. Use `os.path.abspath()` for path. Import the shared client in both loader and retriever.

### BUG 4 — Auth blocks standalone frontend (LOW)
**File**: `api/auth.py`
**Problem**: Frontend hardcodes `Bearer dummy_token`. When real auth is wired in, the frontend silently breaks.
**Fix**: Add `AUTH_BYPASS` env var. When `true` (default for dev), skip all validation.

### BUG 5 — knowledge_base.md chunking may produce 0 chunks (MEDIUM)
**File**: `ingestion/chunker.py` lines 14-22
**Problem**: Splits on a specific separator string (`====...====`, 80 chars). If the actual file uses different formatting, the whole file becomes one giant un-retrievable chunk.
**Fix**: Open `ai-service/data/knowledge_base.md`, check the real separator, and fix the split pattern. Recommended: split both files on `##` headings for consistency.

### BUG 6 — FileResponse uses relative path (LOW)
**File**: `api/main.py` line 88
**Problem**: `FileResponse("frontend/index.html")` depends on CWD being `ai-service/`. Will 404 if run from a different directory.
**Fix**: Use `os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend", "index.html")`.

---

## STEP-BY-STEP PLAN TO GET IT FULLY WORKING

### PHASE 1 — Local bare-Python (priority, no Docker needed)

**Step 1: Install Ollama locally on Windows**
- Download from https://ollama.com/download/windows and install.
- After install, open a terminal and run: `ollama serve`
- Pull a model: `ollama pull llama3` (downloads ~4 GB)
- Verify: `curl http://localhost:11434/api/tags` returns JSON with model list

**Step 2: Apply all bug fixes (Bugs 1-6 above)**

**Step 3: Create `rag/chroma_client.py` (shared singleton)**
```python
import os
import chromadb
from chromadb.utils import embedding_functions
import config

_client = None
_embedding_func = None

def get_chroma_client():
    global _client, _embedding_func
    if _client is None:
        persist_path = os.path.abspath(config.CHROMA_PERSIST_DIR)
        _client = chromadb.PersistentClient(path=persist_path)
        _embedding_func = embedding_functions.DefaultEmbeddingFunction()
    return _client, _embedding_func
```

**Step 4: Restart the server**
```
python -m uvicorn api.main:app --host 127.0.0.1 --port 8080 --reload
```
Watch for "Successfully indexed N chunks." in startup logs (N should be > 5).

**Step 5: Run the test checklist (see below)**

### PHASE 2 — Docker deployment (when Docker is available on the host)

`docker-compose.yml` is already written at `c:\pineaple-rag\docker-compose.yml`.
Launch sequence:
```
docker compose up -d --build
docker exec -it agritech-ollama ollama pull llama3
curl -X POST http://localhost:8080/api/ai/reindex
```
Then open http://localhost:8080/

---

## ALL CURRENT FILE CONTENTS (for reference when editing)

### config.py (NEEDS FIX on line 3)
```python
import os
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")  # CHANGE to http://localhost:11434
OLLAMA_DEFAULT_MODEL = os.getenv("OLLAMA_DEFAULT_MODEL", "llama3")
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_store")
DATA_DIR = os.getenv("DATA_DIR", "./data")
DAILY_BRIEF_CRON_HOUR = int(os.getenv("DAILY_BRIEF_CRON_HOUR", "6"))
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
AUTH_TOKEN_HEADER = os.getenv("AUTH_TOKEN_HEADER", "Authorization")
```

### api/auth.py (NEEDS AUTH_BYPASS)
```python
from fastapi import Header, HTTPException
async def verify_token(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    return authorization
```

### api/main.py (NEEDS asyncio fix and path fix — see lines 33 and 88)
See file at c:\pineaple-rag\ai-service\api\main.py

### ingestion/loader.py (NEEDS shared client refactor)
See file at c:\pineaple-rag\ai-service\ingestion\loader.py

### rag/retriever.py (NEEDS shared client refactor)
See file at c:\pineaple-rag\ai-service\rag\retriever.py

### rag/generator.py (URL comes from config — fixed after Bug 1 fix)
See file at c:\pineaple-rag\ai-service\rag\generator.py

---

## WHAT THE RAG KNOWS (context grounding)

`data/knowledge_base.md` contains scraped Agritech dashboard data:
- Farm 1 (Highland Pineapple, Cameron Highlands): 1,247 ha, Block C-3 NDVI drop 0.18 (18.2 ha affected)
- Farm 2 (Lowland Oil Palm, Sandakan Sabah): 842 ha, Block W-2 pest damage, low sprinkler pressure
- Farm 3 (Coastal Pineapple, Pontian Johor): 1,583 ha, salt stress, early ripening
- All active alerts, GIS data, workforce status, drone missions

`data/rag_system_prompt.md` contains agronomic inference rules:
- NDVI drop > 0.1 ? pest/irrigation failure ? dispatch agronomist
- Coastal stress ? salt stress ? salinity test
- Sprinkler pressure low ? pipe/pump ? maintenance crew
- Early ripening ? pull harvest crew forward
- No imagery > 10 days ? schedule drone survey
- Always tag [CRITICAL]/[HIGH]/[MEDIUM]/[LOW], cite specific block IDs

---

## END-TO-END TEST CHECKLIST

| Test | Expected Result |
|---|---|
| GET http://localhost:8080/ | Dark green chat UI loads |
| Model dropdown on page load | Shows "llama3" |
| GET /api/ai/health | {"status": "healthy"} |
| POST /api/ai/reindex | {"status": "success", "chunks_indexed": N} where N > 0 |
| Chat: "What are the current alerts?" | Lists Block C-3, workforce shortage, Block W-2, salt stress |
| Chat: "What should I do about Block C-3?" | [HIGH] or [CRITICAL] badge, mentions reducing irrigation |
| Chat: "How is Farm 3 doing?" | Mentions coastal/salt stress and early ripening |
| Farm filter set to "Farm 1" | Responses focus on Highland Pineapple Estate |
| Daily Brief button | Returns a generated brief |

---

## IMPORTANT NOTES

1. Do NOT delete `chroma_store/` — it contains already-indexed vectors.
2. The frontend `index.html` is confirmed working — do not redesign it.
3. First Ollama call after pulling a model is slow (model loading into memory). Subsequent calls are fast.
4. Auth is intentionally permissive for now. Real JWT integration is a future task.
5. The `rag_system_prompt.md` is loaded as the SYSTEM prompt for every Ollama call — this is intentional and grounding.
6. Timeout for Ollama is set to 60 seconds in generator.py. Increase if using large models like llama3:70b.

## PRIORITY ORDER FOR FIXES

1. config.py — Ollama URL (Bug 1) — MUST FIX FIRST
2. api/main.py — asyncio.create_task (Bug 2)
3. rag/chroma_client.py — NEW singleton file (Bug 3)
4. ingestion/loader.py + rag/retriever.py — use shared client (Bug 3)
5. api/auth.py — AUTH_BYPASS flag (Bug 4)
6. ingestion/chunker.py — verify separator in knowledge_base.md (Bug 5)
7. api/main.py — absolute path for FileResponse (Bug 6)
