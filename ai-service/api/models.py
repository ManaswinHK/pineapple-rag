from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ChatRequest(BaseModel):
    query: str
    model: Optional[str] = None
    farm_filter: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
    sources: List[str]
    model_used: str
    severity: Optional[str] = None

class ModelsResponse(BaseModel):
    models: List[str]

class DailyBriefResponse(BaseModel):
    brief: str
    generated_at: datetime
    model_used: str

class ReindexResponse(BaseModel):
    status: str
    chunks_indexed: int
