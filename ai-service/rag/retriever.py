import chromadb
from chromadb.utils import embedding_functions
import config

from .chroma_client import get_chroma_client

def retrieve_context(query: str, farm_filter: str = None, top_k: int = 5):
    chroma_client, embedding_func = get_chroma_client()
    try:
        collection = chroma_client.get_collection(name="agritech_knowledge", embedding_function=embedding_func)
    except Exception:
        # Collection might not exist yet
        return []
        
    where_clause = None
    if farm_filter:
        where_clause = {"farm": farm_filter} # Assuming future chunks have this metadata
        
    results = collection.query(
        query_texts=[query],
        n_results=top_k,
        where=where_clause
    )
    
    contexts = []
    if results['documents'] and results['documents'][0]:
        for doc, meta in zip(results['documents'][0], results['metadatas'][0]):
            source_info = meta.get('source', 'unknown')
            extra = meta.get('section', meta.get('url', ''))
            contexts.append(f"Source: {source_info} - {extra}\n{doc}")
            
    return contexts
