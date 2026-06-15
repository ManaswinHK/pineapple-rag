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
