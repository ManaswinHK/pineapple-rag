import os

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_DEFAULT_MODEL = os.getenv("OLLAMA_DEFAULT_MODEL", "llama3")
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_store")
DATA_DIR = os.getenv("DATA_DIR", "./data")
DAILY_BRIEF_CRON_HOUR = int(os.getenv("DAILY_BRIEF_CRON_HOUR", "6"))
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
AUTH_TOKEN_HEADER = os.getenv("AUTH_TOKEN_HEADER", "Authorization")
