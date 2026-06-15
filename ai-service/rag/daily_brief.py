from datetime import datetime
from .generator import generate_response

# Store the latest brief in memory for simplicity
LATEST_BRIEF = None

async def generate_daily_brief():
    global LATEST_BRIEF
    query = "Generate today's intelligence brief covering all active alerts, vegetation changes, workforce status, and recommended actions across all farms."
    
    response = await generate_response(query=query)
    
    LATEST_BRIEF = {
        "brief": response["answer"],
        "generated_at": datetime.now(),
        "model_used": response["model_used"]
    }
    return LATEST_BRIEF

def get_latest_brief():
    global LATEST_BRIEF
    if LATEST_BRIEF is None:
        return {
            "brief": "The daily intelligence brief has not been generated yet. Please wait for the next scheduled run or trigger it manually.",
            "generated_at": datetime.now(),
            "model_used": "N/A"
        }
    return LATEST_BRIEF
