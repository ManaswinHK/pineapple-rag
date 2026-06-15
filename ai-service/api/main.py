from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import os

import config
from .models import ChatRequest, ChatResponse, ModelsResponse, DailyBriefResponse, ReindexResponse
from .auth import verify_token
from ingestion.loader import load_and_index
from rag.generator import generate_response, list_models
from rag.daily_brief import generate_daily_brief, get_latest_brief

scheduler = AsyncIOScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Load and index data into ChromaDB
    print("Starting up... indexing data.")
    try:
        load_and_index()
    except Exception as e:
        print(f"Error indexing on startup: {e}")
        
    # Start the scheduler for the daily brief
    scheduler.add_job(generate_daily_brief, 'cron', hour=config.DAILY_BRIEF_CRON_HOUR, minute=0)
    scheduler.start()
    
    # Generate the first brief right away
    from datetime import datetime, timedelta
    scheduler.add_job(generate_daily_brief, 'date', run_date=datetime.now() + timedelta(seconds=10))
    
    yield
    # Shutdown
    scheduler.shutdown()

app = FastAPI(title="Agritech AI Analysis Service", lifespan=lifespan)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routes
@app.post("/api/ai/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, token: str = Depends(verify_token)):
    response_data = await generate_response(
        query=request.query,
        model=request.model,
        farm_filter=request.farm_filter
    )
    return ChatResponse(**response_data)

from fastapi.responses import StreamingResponse
from rag.generator import generate_response_stream

@app.post("/api/ai/chat/stream")
async def chat_stream_endpoint(request: ChatRequest, token: str = Depends(verify_token)):
    return StreamingResponse(
        generate_response_stream(
            query=request.query,
            model=request.model,
            farm_filter=request.farm_filter
        ),
        media_type="application/x-ndjson"
    )

@app.get("/api/ai/daily-brief", response_model=DailyBriefResponse)
async def daily_brief_endpoint(token: str = Depends(verify_token)):
    brief_data = get_latest_brief()
    return DailyBriefResponse(**brief_data)

@app.get("/api/ai/models", response_model=ModelsResponse)
async def models_endpoint(token: str = Depends(verify_token)):
    models = await list_models()
    return ModelsResponse(models=models)

@app.post("/api/ai/reindex", response_model=ReindexResponse)
async def reindex_endpoint(token: str = Depends(verify_token)):
    try:
        count = load_and_index()
        return ReindexResponse(status="success", chunks_indexed=count)
    except Exception as e:
        return ReindexResponse(status="error", chunks_indexed=0)

@app.get("/api/ai/health")
async def health_check():
    return {"status": "healthy"}

# Serve Frontend
os.makedirs("frontend", exist_ok=True)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
async def serve_frontend():
    frontend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend", "index.html")
    return FileResponse(frontend_path)
