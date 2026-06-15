import os
from fastapi import Header, HTTPException

AUTH_BYPASS = os.getenv("AUTH_BYPASS", "true").lower() == "true"

async def verify_token(authorization: str = Header(None)):
    if AUTH_BYPASS:
        return "dev"
        
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    return authorization
