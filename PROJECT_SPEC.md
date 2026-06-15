# Agritech RAG AI Analysis Service — Complete Project Specification

> **Purpose**: This document contains ALL context, architecture, data, and specifications needed to build the deployable RAG-based AI Analysis Service for the Agritech pineapple farm management platform. Feed this to your LLM of choice to generate the full codebase.

---

## TABLE OF CONTENTS
1. [Project Overview](#1-project-overview)
2. [Existing System Architecture](#2-existing-system-architecture)
3. [Scraped Website Data (Knowledge Base)](#3-scraped-website-data)
4. [Technology Decisions](#4-technology-decisions)
5. [File Structure](#5-file-structure)
6. [Backend Specification](#6-backend-specification)
7. [RAG Pipeline Specification](#7-rag-pipeline-specification)
8. [API Contract](#8-api-contract)
9. [Frontend Specification](#9-frontend-specification)
10. [Docker & Deployment](#10-docker--deployment)
11. [RAG System Prompt (Agronomic Logic)](#11-rag-system-prompt)

---

## 1. PROJECT OVERVIEW

**What**: A deployable microservice that provides a RAG-based AI chat assistant for plantation estate managers. It answers questions about farm health, suggests operational actions, and generates daily intelligence briefs — all grounded in real farm data (vegetation indices, alerts, drone surveys, workforce).

**Who uses it**: Estate managers, agronomists, and drone operators managing pineapple and oil palm plantations in Malaysia.

**Key behaviors**:
- User asks a question → AI retrieves relevant farm data from vector store + live context → generates an actionable, severity-tagged response.
- Daily at 06:00, auto-generates an intelligence brief from all active alerts, vegetation changes, and workforce gaps.
- User can switch between Ollama models (e.g., llama3, mistral, gemma2) from the UI.

---

## 2. EXISTING SYSTEM ARCHITECTURE

### 2.1 Overall Architecture (from whiteboard)

The platform is composed of independent microservices. Every service runs on the same server, stores data in a shared MinIO (object storage) and PostgreSQL (relational database).

```
Our Software
├── Upload Service
├── Orthomosaic Service
├── Plant Detection Service
├── Vegetation Index Service
├── AI Analysis Service          ← THIS IS WHAT WE'RE BUILDING
└── Additional Services
    ├── Tile Server
    └── Miscellaneous (Login, Storage)
```

**Storage Layer**:
- **MinIO**: Handles large file storage (raw images, orthomosaics, GeoTIFFs, CSV outputs).
- **PostgreSQL**: Handles metadata storage (plant coordinates, health statuses, vegetation indices, alerts, workforce data).

**Control Layer**: A single REST API fronts all services.

### 2.2 Data Processing Pipeline (sequential, each triggers the next)

```
Upload Service
→ Orthomosaic Service
  → Plant Detection Service
    → Vegetation Index Service
      → AI Analysis Service (consumes final outputs)
```

**Step-by-step**:

1. **Upload Service**
   - Uploads raw files onto MinIO from the frontend.
   - Input: Multispectral images (.tif), RGB images (.jpeg)
   - All images stored in object storage.
   - Automatically triggers the Orthomosaic Service.

2. **Orthomosaic Service**
   - Converts raw images into GeoTIFF orthomosaics using a Python script running WebODM.
   - Output: 8 Health Maps, Ortho DSM (Digital Surface Model), DTM (Digital Terrain Model).
   - Stores outputs in MinIO.
   - Deletes raw images from object storage or retains if required.
   - Automatically triggers the Plant Detection Service.

3. **Plant Detection Service**
   - Takes the orthomosaic map as input from object storage.
   - Detects plants and other miscellaneous data.
   - Output: A single CSV/JSON file with pixel coordinates of each plant and other miscellaneous metadata.
   - Stores output in object storage.
   - Automatically triggers the Vegetation Index Service.

4. **Vegetation Index Service**
   - Takes in the orthomosaic map and other multispectral images.
   - Calculates vegetation indexes (NDVI, NDRE, etc.).
   - Output: Orthomosaic maps for each vegetation index AND metadata of the indexes as CSV files.
   - CSV/JSON contains: color, index values, health status of EACH plant.
   - Stored in object storage.

5. **AI Analysis Service** (what we build)
   - Consumes structured metadata from PostgreSQL and CSV/JSON files from MinIO.
   - Generates actionable agronomic insights via RAG.

### 2.3 Key Architecture Rules
- Every service is an independent service running on the server.
- Each service stores and manages data in the object storage and the PostgreSQL database.
- One-time or maintenance required services are noted separately.

---

## 3. SCRAPED WEBSITE DATA

This is the full text content extracted from every page of the Agritech dashboard at https://roots-and-rays.vercel.app/. Use this as the static knowledge base for the RAG system.

### 3.1 Dashboard (Homepage)

- Platform name: **Agritech** — Farm Intelligence Platform
- Tagline: "Enterprise agricultural intelligence for plantation operators, agronomists and drone teams."
- Current user: **Nishit DB**, role: **Estate Manager**
- Season: **25/26 · Week 41**

**Portfolio Summary** (3 farms):
- Total area: **3,672 ha**
- Total plants: **8.03 M**
- Healthy canopy: **85.5%**
- Avg yield forecast: **61.7 t/ha**
- Year-over-year growth: **+7.4% YoY**

**Farm 1: Highland Pineapple Estate**
- Location: Cameron Highlands, Pahang
- Coordinates: 18°N 121°E
- Crop: Pineapple
- Area: 1,247 ha
- Plants: 2.74M
- Healthy: 86.4%
- Yield: 61.4 t/ha
- Blocks: 38
- Established: 2009

**Farm 2: Lowland Oil Palm Estate**
- Location: Sandakan, Sabah
- Coordinates: 18°N 121°E
- Crop: Oil Palm
- Area: 842 ha
- Plants: 1.83M
- Healthy: 78.1%
- Yield: 54.8 t/ha
- Blocks: 26
- Established: 2014

**Farm 3: Coastal Pineapple Estate**
- Location: Pontian, Johor
- Coordinates: 18°N 121°E
- Crop: Pineapple
- Area: 1,583 ha
- Plants: 3.46M
- Healthy: 91.2%
- Yield: 68.9 t/ha
- Blocks: 47
- Established: 2005

**AI Recommendations (today)**:
1. Farm 3: Pull harvest crew forward to August — Crop ripening ahead of plan.
2. Farm 2: Inspect Block W-2 for pest damage — Cluster of stressed plants detected.
3. Farm 1: Reduce irrigation on Block C-3 — Soil too wet after recent rain.

**Recent Alerts**:
1. Farm 1: Severe stress in Block C-3 — High priority · 2h ago
2. Farm 2: Severe stress patch in Block W-2 — High priority · 1h ago
3. Farm 3: Salt stress near shore — Medium priority · 3h ago
4. Farm 2: Sprinkler pressure low — Medium priority · 4h ago
5. Farm 1: Drone survey completed — Low priority · 1d ago

---

### 3.2 GIS Mapping

- Interactive layered map of the selected estate.
- Available layers: Composite, NDVI, NDRE, Health, Terrain, Yield
- Active layer: Composite
- Showing: Farm 1 · last capture 6 Jun 2026
- Opacity control available.
- Date history:
  - 6 Jun 2026 · Mission MX-218
  - 30 May 2026 · Mission MX-212
  - 22 May 2026 · Mission MX-207
- Legend: Healthy, Mild stress, Severe stress, Bare ground
- Export: GeoTIFF export available

---

### 3.3 Workforce

- Status: **In development · ETA Q3 2026**
- Description: An end-to-end workforce module for plantation crews, supervisors and payroll.
- Planned features:
  1. Worker directory and teams — Roster, certifications, contact, daily availability.
  2. Attendance and timesheets — Mobile clock-in, geofenced jobsites, exception flags.
  3. Task assignments — Assign block-level tasks to crews with progress tracking.
  4. Productivity analytics — Per-team output, harvest pace, anomaly detection.

---

### 3.4 Drone Operations

- Status: **In development · ETA Q3 2026**
- Description: Mission planning, telemetry and fleet management for the agronomy drone program.
- Planned features:
  1. Mission planner — Auto-generate flight paths per block with overlap, altitude, sidelap controls.
  2. Live flight telemetry — Battery, GPS lock, payload status across the active fleet.
  3. Fleet and equipment — Airframe hours, sensor calibration, maintenance scheduling.
  4. Survey history — Searchable archive of every capture with ortho previews.

---

### 3.5 Alert Center

- Description: Prioritised events from agronomy models, operations and field reports.
- Features: Configure thresholds, Mark all read, Resolve individual alerts.
- Active alerts:
  1. **Severe stress detected · Block C-3** — Critical · AI · imagery — "NDVI dropped 0.18 since last capture. Affects 18.2 ha." — 2h ago
  2. **Workforce shortage forecast** — High · Roster system — "Wednesday roster shows -12 workers vs harvest schedule." — 5h ago
  3. **Yield decline · Block B-1** — Medium · Forecast model — "Projection revised -4.2 t/ha for harvest window." — yesterday
  4. **Missed survey · Block 5** — Medium · Operations — "No imagery in 12 days. Auto-scheduled for tomorrow 06:00." — yesterday
  5. **Mission MX-218 completed** — Low · Drone Ops — "412 ha processed. New layers available." — 1d ago
  6. **5 tasks closed today** — Low · Task system — "Bravo team completed harvest sector 3 ahead of schedule." — 1d ago

---

### 3.6 Data Management

- Datasets: 184 across estate
- Storage used: 612 GB of 2 TB
- Processing queue: 3 queued
- Last sync: 12 min ago
- Upload types: Raw, multispectral, thermal or RGB captures
- Import types: Shapefiles, GeoJSON, KML, GeoTIFF
- Connect: Sensors, weather stations, ERP exports

**Datasets table**:
| Name | Type | Size | Source | Status |
|---|---|---|---|---|
| Estate orthomosaic · 6 Jun 2026 | GeoTIFF | 4.2 GB | MX-218 | Processed |
| NDVI composite · 6 Jun 2026 | GeoTIFF | 812 MB | MX-218 | Processed |
| Terrain scan · Sector 5 | GeoTIFF | 1.1 GB | MX-198 | Processing |
| Field boundaries · 2026 | Shapefile | 12 MB | GIS team | Active |
| Harvest records · May 2026 | CSV | 184 KB | Field forms | Active |

---

### 3.7 Settings

- Tabs: Organisation, Users and permissions, Notifications, Preferences
- Fields: Organisation name, Trading entity, Primary estate, Headquarters

---

### 3.8 Profile

- User: Nishit DB
- Role: Estate Manager (Owner)
- Account fields: Full name, Role, Email, Phone, Location
- Email preferences: Configurable Agritech notification settings
- Security: Password, 2FA, trusted devices
- Default farm: Set the farm to land on after sign-in
- Active sessions:
  - MacBook Pro · Chrome — Kuala Lumpur, Malaysia · Active now
  - iPhone 15 · Safari — Pontian, Johor · 2 days ago

---

### 3.9 Navigation Structure

**Sidebar sections**:
- **Overview**: Dashboard
- **Intelligence**: Farm Intelligence (expandable), GIS Mapping
- **Operations**: Workforce, Drone Operations
- **Insights**: Reports (expandable), Alerts
- **System**: Data Management, Settings

---

## 4. TECHNOLOGY DECISIONS

| Decision | Choice | Reason |
|---|---|---|
| LLM Provider | **Self-hosted Ollama** | No API costs, data stays on-premise, variable model selection |
| Model Selection | **User picks per request** (llama3, mistral, gemma2, etc.) | Flexibility |
| Vector Database | **ChromaDB** (embedded/persistent mode) | PostgreSQL does not have pgvector; ChromaDB requires zero infra |
| Embeddings | **ChromaDB default** (all-MiniLM-L6-v2 via onnxruntime) | Ships with ChromaDB, no extra dependency |
| Backend Framework | **FastAPI** (Python) | Async, fast, matches existing Python microservices |
| Frontend | **Standalone HTML page** | Simplicity; not integrated into the React dashboard yet |
| Auth | **Same auth as other services** | Share the existing login/token system |
| Deployment | **Docker** (docker-compose) | Matches existing microservice deployment pattern |

---

## 5. FILE STRUCTURE

```
ai-service/
├── Dockerfile
├── requirements.txt
├── config.py                    # All env vars, defaults, constants
├── api/
│   ├── __init__.py
│   ├── main.py                  # FastAPI app, CORS, routes, startup events
│   ├── models.py                # Pydantic schemas for request/response
│   └── auth.py                  # Auth middleware (shared token validation)
├── ingestion/
│   ├── __init__.py
│   ├── chunker.py               # Split documents into chunks
│   └── loader.py                # Load files, call chunker, store in ChromaDB
├── rag/
│   ├── __init__.py
│   ├── retriever.py             # ChromaDB similarity search
│   ├── generator.py             # Ollama HTTP client, prompt assembly
│   └── daily_brief.py           # Scheduled auto-generated intelligence brief
├── data/
│   ├── knowledge_base.md        # Scraped website content (Section 3 above)
│   └── rag_system_prompt.md     # Agronomic logic and tone rules (Section 11)
├── chroma_store/                # Persistent ChromaDB data (Docker volume)
└── frontend/
    └── index.html               # Standalone chat page (served by FastAPI)

docker-compose.yml               # ai-service + ollama containers
```

---

## 6. BACKEND SPECIFICATION

### 6.1 config.py
```python
# Environment variables with defaults
OLLAMA_BASE_URL = "http://ollama:11434"    # Docker service name
OLLAMA_DEFAULT_MODEL = "llama3"
CHROMA_PERSIST_DIR = "./chroma_store"
DATA_DIR = "./data"
DAILY_BRIEF_CRON_HOUR = 6                  # 06:00 local time
CORS_ORIGINS = ["*"]                       # Tighten in production
AUTH_TOKEN_HEADER = "Authorization"         # Same as other services
```

### 6.2 api/models.py — Pydantic Schemas
```
ChatRequest:
  - query: str (required)
  - model: str (optional, default from config)
  - farm_filter: str or None (optional — "Farm 1", "Farm 2", etc.)

ChatResponse:
  - answer: str
  - sources: list[str]          # Which chunks were used
  - model_used: str
  - severity: str or None       # CRITICAL / HIGH / MEDIUM / LOW if applicable

ModelsResponse:
  - models: list[str]           # Available Ollama models

DailyBriefResponse:
  - brief: str
  - generated_at: datetime
  - model_used: str

ReindexResponse:
  - status: str
  - chunks_indexed: int
```

### 6.3 api/auth.py
- Middleware or dependency that extracts the auth token from the Authorization header.
- Validates it against the same mechanism used by other services (e.g., JWT verification or session check against PostgreSQL).
- Returns 401 if invalid.

### 6.4 ingestion/chunker.py — Chunking Strategy
- **Markdown files** (knowledge_base.md, rag_system_prompt.md):
  - Split by === separator (each page becomes a chunk) for knowledge_base.md.
  - Split by ## headings for rag_system_prompt.md.
  - Each chunk gets metadata: {source: "knowledge_base", url: "...", section: "..."}.
- **CSV/JSON data** (from Vegetation Index / Plant Detection — future):
  - Group rows by Block → one chunk per block with summary stats.
  - Metadata: {source: "vegetation_index", farm: "Farm 1", block: "C-3", date: "2026-06-06"}.
- **Alerts** (from PostgreSQL — future):
  - One chunk per alert with full context.
  - Metadata: {source: "alert", severity: "critical", farm: "Farm 1"}.
- **Chunk size**: approximately 500 tokens max, 50-token overlap for markdown splits.

### 6.5 ingestion/loader.py
- On startup (or manual trigger via /api/ai/reindex):
  1. Reads all .md files from data/ directory.
  2. Calls chunker.py to split them.
  3. Upserts chunks into ChromaDB collection "agritech_knowledge".
  4. Returns count of chunks indexed.
- Future: also pulls latest CSV/JSON from MinIO and alert records from PostgreSQL.

### 6.6 rag/retriever.py
- Takes a query string and optional farm filter.
- Embeds the query using ChromaDB default embedding function.
- Performs cosine similarity search, returns top 5-8 chunks.
- If farm_filter is set, adds a where clause on metadata: {"farm": farm_filter}.
- Returns list of (chunk_text, metadata, distance).

### 6.7 rag/generator.py
- **Ollama client**: HTTP calls to OLLAMA_BASE_URL/api/chat (streaming) or /api/generate.
- **Model listing**: GET OLLAMA_BASE_URL/api/tags → returns available models.
- **Prompt assembly**:
  ```
  SYSTEM: {contents of rag_system_prompt.md}

  CONTEXT FROM KNOWLEDGE BASE:
  ---
  {chunk 1}
  ---
  {chunk 2}
  ---
  ... (top-k retrieved chunks)

  USER QUESTION: {user query}

  Respond with actionable advice. Tag severity as [CRITICAL], [HIGH], [MEDIUM], or [LOW].
  Cite specific farms, blocks, and data points.
  ```
- Calls Ollama /api/chat endpoint with the assembled messages.
- Parses the response and extracts severity tag if present.

### 6.8 rag/daily_brief.py
- Runs on a schedule (APScheduler, cron-like, daily at 06:00).
- Constructs a special query: "Generate today's intelligence brief covering all active alerts, vegetation changes, workforce status, and recommended actions across all farms."
- Runs through the same retriever → generator pipeline.
- Stores the result in memory (or a file/DB) for the GET endpoint.

### 6.9 api/main.py
- FastAPI app with:
  - CORS middleware.
  - Auth dependency.
  - on_event("startup") → runs the loader to index data into ChromaDB + starts the daily brief scheduler.
  - Serves the frontend/index.html as a static file at /.
  - All API routes under /api/ai/.

---

## 7. RAG PIPELINE SPECIFICATION

### Query Flow (step by step)

```
User types: "What's wrong with Block C-3?"
    |
    v
[1] FastAPI receives POST /api/ai/chat
    Body: { query: "What's wrong with Block C-3?", model: "llama3" }
    |
    v
[2] Retriever embeds the query → searches ChromaDB
    Returns top 5 chunks:
      - Alert: "Severe stress in Block C-3, NDVI dropped 0.18..."
      - Dashboard: "Farm 1, Highland Pineapple Estate, 86.4% healthy..."
      - Recommendation: "Reduce irrigation on Block C-3, soil too wet..."
      - System prompt chunk: "Irrigation and Weather inference rules..."
      - GIS data: "Last capture 6 Jun 2026, layers: NDVI, NDRE..."
    |
    v
[3] Generator assembles the prompt:
    SYSTEM: [rag_system_prompt.md content]
    CONTEXT: [5 retrieved chunks]
    USER: "What's wrong with Block C-3?"
    |
    v
[4] Ollama (llama3) generates response:
    "[HIGH] Block C-3 in Farm 1 (Highland Pineapple Estate) is showing
     severe vegetation stress. NDVI dropped by 0.18 since the last
     drone capture on 6 Jun 2026, affecting 18.2 ha.

     Recommended actions:
     1. Reduce irrigation immediately — soil moisture is elevated
        after recent rainfall, risking root rot.
     2. Dispatch an agronomist to inspect for pest damage or disease.
     3. Schedule a follow-up drone survey within 3 days to track
        recovery after intervention."
    |
    v
[5] Response returned to frontend with sources and severity tag.
```

---

## 8. API CONTRACT

### Endpoints

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | /api/ai/chat | Yes | Send a question, get AI response |
| GET | /api/ai/daily-brief | Yes | Get latest auto-generated brief |
| GET | /api/ai/models | Yes | List available Ollama models |
| POST | /api/ai/reindex | Yes | Re-ingest all data into ChromaDB |
| GET | /api/ai/health | No | Health check |
| GET | / | No | Serve the standalone chat HTML page |

### POST /api/ai/chat — Request
```json
{
  "query": "What should I prioritize today?",
  "model": "llama3",
  "farm_filter": null
}
```

### POST /api/ai/chat — Response
```json
{
  "answer": "[CRITICAL] Immediate attention needed on Farm 1, Block C-3...",
  "sources": [
    "knowledge_base.md — Dashboard alerts",
    "knowledge_base.md — GIS Mapping"
  ],
  "model_used": "llama3",
  "severity": "CRITICAL"
}
```

### GET /api/ai/models — Response
```json
{
  "models": ["llama3", "llama3:70b", "mistral", "gemma2", "phi3"]
}
```

### GET /api/ai/daily-brief — Response
```json
{
  "brief": "## Daily Intelligence Brief — 15 Jun 2026\n\n### [CRITICAL] Farm 1...",
  "generated_at": "2026-06-15T06:00:00+08:00",
  "model_used": "llama3"
}
```

---

## 9. FRONTEND SPECIFICATION

### Standalone Chat Page (frontend/index.html)

**Design requirements** (single HTML file with inline CSS and JS):

- **Dark theme** with the Agritech brand colors:
  - Background: #0f1a12 (deep forest)
  - Card/panel: #1a2e1f with rgba(255,255,255,0.06) border
  - Accent green (sage): #6b8f71
  - Alert colors: Critical = #ef4444, High = #f97316, Medium = #eab308, Low = #22c55e
- **Font**: Inter (Google Fonts)
- **Layout**:
  - Top bar: Agritech logo (leaf icon + "Agritech" text), model selector dropdown, connection status indicator.
  - Main area: Scrollable chat messages. AI messages rendered as markdown with severity badges. User messages right-aligned.
  - Bottom: Input bar with placeholder "Ask about your farms...", send button, farm filter dropdown (All Farms / Farm 1 / Farm 2 / Farm 3).
- **Features**:
  - Model selector dropdown: Fetches available models from GET /api/ai/models on page load.
  - Markdown rendering in AI responses (use a lightweight lib like marked.js from CDN).
  - Severity badges: Parse [CRITICAL], [HIGH], [MEDIUM], [LOW] from response and render as colored badges.
  - Loading state: Pulsing dot animation while waiting for response.
  - Auto-scroll to latest message.
  - Responsive: works on desktop and tablet.

---

## 10. DOCKER AND DEPLOYMENT

### docker-compose.yml

```yaml
version: "3.8"

services:
  ollama:
    image: ollama/ollama:latest
    container_name: agritech-ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    restart: unless-stopped
    # GPU support (uncomment if NVIDIA GPU available):
    # deploy:
    #   resources:
    #     reservations:
    #       devices:
    #         - driver: nvidia
    #           count: all
    #           capabilities: [gpu]

  ai-service:
    build: ./ai-service
    container_name: agritech-ai
    ports:
      - "8080:8080"
    environment:
      - OLLAMA_BASE_URL=http://ollama:11434
      - OLLAMA_DEFAULT_MODEL=llama3
      - CHROMA_PERSIST_DIR=/app/chroma_store
      - DATA_DIR=/app/data
    volumes:
      - chroma_data:/app/chroma_store
      - ./ai-service/data:/app/data
    depends_on:
      - ollama
    restart: unless-stopped

volumes:
  ollama_data:
  chroma_data:
```

### ai-service/Dockerfile

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

### ai-service/requirements.txt

```
fastapi>=0.111.0
uvicorn[standard]>=0.30.0
chromadb>=0.5.0
httpx>=0.27.0
pydantic>=2.0
apscheduler>=3.10.0
python-multipart
```

### First-time setup after docker-compose up:

```bash
# 1. Pull a model into Ollama
docker exec -it agritech-ollama ollama pull llama3

# 2. (Optional) Pull more models
docker exec -it agritech-ollama ollama pull mistral
docker exec -it agritech-ollama ollama pull gemma2

# 3. Trigger initial indexing
curl -X POST http://localhost:8080/api/ai/reindex

# 4. Open the chat
# Navigate to http://localhost:8080/
```

---

## 11. RAG SYSTEM PROMPT (Agronomic Logic)

This is the full system prompt that gets prepended to every LLM call. It teaches the AI how the platform works and how to reason about farm data.

```
You are the Agritech AI Assistant — an expert agronomist AI embedded in the Agritech Farm Intelligence Platform. You help estate managers, agronomists, and drone operators make data-driven decisions about their plantations.

## YOUR KNOWLEDGE OF THE SYSTEM

### Architecture and Data Flow
The platform processes drone imagery through this pipeline:
1. Upload Service: Raw .tif (multispectral) and .jpeg (RGB) images are uploaded to MinIO object storage.
2. Orthomosaic Service: WebODM converts raw images into GeoTIFF orthomosaics, producing DSM, DTM, and 8 health maps.
3. Plant Detection Service: Analyzes orthomosaics to detect individual plants. Outputs CSV/JSON with pixel coordinates, plant count, and area.
4. Vegetation Index Service: Calculates NDVI, NDRE, and other indices per plant. Outputs GeoTIFF maps and CSV/JSON with color, index score, and health status of each plant.
5. You (AI Analysis Service): Consume all this structured data to generate insights.

### Storage
- MinIO: Large files (orthomosaics, GeoTIFFs, raw imagery)
- PostgreSQL: Metadata (plant data, alerts, workforce, indices)

## FARM PORTFOLIO

### Farm 1: Highland Pineapple Estate
- Location: Cameron Highlands, Pahang (high elevation, cooler climate)
- Area: 1,247 ha | Plants: 2.74M | Healthy: 86.4% | Yield: 61.4 t/ha
- 38 blocks | Established 2009
- Key concern: Block C-3 showing severe stress (NDVI drop 0.18, 18.2 ha affected)

### Farm 2: Lowland Oil Palm Estate
- Location: Sandakan, Sabah (lowland, tropical)
- Area: 842 ha | Plants: 1.83M | Healthy: 78.1% | Yield: 54.8 t/ha
- 26 blocks | Established 2014
- Key concerns: Block W-2 pest damage, sprinkler pressure low

### Farm 3: Coastal Pineapple Estate
- Location: Pontian, Johor (coastal, salt stress risk)
- Area: 1,583 ha | Plants: 3.46M | Healthy: 91.2% | Yield: 68.9 t/ha
- 47 blocks | Established 2005
- Key concern: Salt stress near shore, crop ripening ahead of schedule

### Portfolio Totals
- Total area: 3,672 ha | Total plants: 8.03M | Avg healthy: 85.5% | Avg yield: 61.7 t/ha | +7.4% YoY

## INFERENCE RULES

When you detect data anomalies, apply these rules:

### Crop Health
- Rapid NDVI/NDRE drop (>0.1) or "Severe stress" cluster → Likely pest damage, disease, or irrigation failure → Recommend: dispatch agronomist, review irrigation schedules.
- Stress in coastal farms → Potential salt stress → Recommend: soil salinity testing, drainage adjustment.

### Irrigation
- High soil moisture + increasing stress → Waterlogging / root rot → Recommend: reduce irrigation, inspect drainage.
- "Sprinkler pressure low" alert → Pipe leak or pump failure → Recommend: dispatch maintenance crew.

### Harvest and Yield
- Early ripening indicators (color/index changes) → Risk of over-ripening → Recommend: pull harvest crew forward, reallocate workforce.
- Yield forecast revised downward → Environmental stress impact → Recommend: adjust logistics, notify off-takers.

### Workforce
- Roster deficit vs. harvest schedule → Labor shortage risk → Recommend: approve overtime or deploy contract labor.
- No drone imagery >10 days → Intelligence blind spot → Recommend: auto-schedule survey flight.

## RESPONSE RULES

1. Start with the severity tag: [CRITICAL], [HIGH], [MEDIUM], or [LOW].
2. Be direct and action-oriented. Lead with what to do, then explain why.
3. Always cite specific data: farm name, block ID, crop type, index values, hectares affected.
4. Never give generic farming advice. Ground everything in THIS platform's data.
5. If you don't have enough data to answer confidently, say so and suggest what data to collect.
6. For multi-farm questions, organize by farm with clear headings.
7. When suggesting actions, consider workforce availability and drone survey schedules.
```

---

## END OF SPECIFICATION

This document contains everything needed to build the complete AI Analysis Service. All scraped data, architecture context, technology choices, API contracts, frontend design, Docker config, and the agronomic system prompt are included above.
