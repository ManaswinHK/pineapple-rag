import os
import chromadb
from chromadb.utils import embedding_functions
from .chunker import chunk_markdown
import config

from rag.chroma_client import get_chroma_client

def load_and_index():
    chroma_client, embedding_func = get_chroma_client()
    collection = chroma_client.get_or_create_collection(name="agritech_knowledge", embedding_function=embedding_func)
    
    # Clear existing to avoid duplicates on re-index for simplicity
    existing = collection.get()
    if existing['ids']:
        collection.delete(ids=existing['ids'])
    
    data_dir = config.DATA_DIR
    files = [f for f in os.listdir(data_dir) if f.endswith('.md') and f != "rag_system_prompt.md"]
    
    total_chunks = 0
    all_documents = []
    all_metadatas = []
    all_ids = []
    
    for filename in files:
        filepath = os.path.join(data_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        chunks = chunk_markdown(content, source=filename)
        for i, chunk in enumerate(chunks):
            doc_id = f"{filename}_chunk_{i}"
            all_documents.append(chunk["text"])
            all_metadatas.append(chunk["metadata"])
            all_ids.append(doc_id)
            
    if all_documents:
        collection.add(
            documents=all_documents,
            metadatas=all_metadatas,
            ids=all_ids
        )
        total_chunks = len(all_ids)
        print(f"Successfully indexed {total_chunks} chunks.")
        
    return total_chunks
