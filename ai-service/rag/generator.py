import httpx
import config
from .retriever import retrieve_context
import json

async def generate_response(query: str, model: str = None, farm_filter: str = None):
    model = model or config.OLLAMA_DEFAULT_MODEL
    
    # 1. Retrieve context
    contexts = retrieve_context(query, farm_filter=farm_filter)
    context_str = "\n\n---\n\n".join(contexts)
    
    # 2. Assemble prompt
    system_prompt = "You are the Agritech AI Assistant. Use the provided context to answer."
    
    # Try to load the actual system prompt if available
    try:
        with open(f"{config.DATA_DIR}/rag_system_prompt.md", "r", encoding="utf-8") as f:
            system_prompt = f.read()
    except FileNotFoundError:
        pass
        
    prompt = f"""
[START OF KNOWLEDGE BASE CONTEXT]
{context_str}
[END OF KNOWLEDGE BASE CONTEXT]

USER QUESTION: {query}

INSTRUCTIONS:
1. ONLY use the data provided in the [START OF KNOWLEDGE BASE CONTEXT] block above.
2. If the answer is not in the context, say "I do not have enough data to answer that."
3. Do not mix data between different farms or blocks.
4. Respond with actionable advice and tag severity as [CRITICAL], [HIGH], [MEDIUM], or [LOW] if applicable.
"""

    # 3. Call Ollama
    ollama_url = f"{config.OLLAMA_BASE_URL}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "system": system_prompt,
        "stream": False
    }
    
    try:
        async with httpx.AsyncClient(timeout=300.0) as client:
            response = await client.post(ollama_url, json=payload)
            response.raise_for_status()
            data = response.json()
            answer = data.get("response", "")
            
            # Extract severity
            severity = None
            for tag in ["[CRITICAL]", "[HIGH]", "[MEDIUM]", "[LOW]"]:
                if tag in answer.upper():
                    severity = tag.strip("[]")
                    break
                    
            # Extract sources
            sources = [c.split('\n')[0] for c in contexts]
            
            return {
                "answer": answer,
                "sources": list(set(sources)),
                "model_used": model,
                "severity": severity
            }
    except Exception as e:
        return {
            "answer": f"Error calling Ollama: {str(e)}",
            "sources": [],
            "model_used": model,
            "severity": None
        }

async def generate_response_stream(query: str, model: str = None, farm_filter: str = None):
    model = model or config.OLLAMA_DEFAULT_MODEL
    
    contexts = retrieve_context(query, farm_filter=farm_filter)
    context_str = "\n\n---\n\n".join(contexts)
    
    system_prompt = "You are the Agritech AI Assistant. Use the provided context to answer."
    try:
        with open(f"{config.DATA_DIR}/rag_system_prompt.md", "r", encoding="utf-8") as f:
            system_prompt = f.read()
    except FileNotFoundError:
        pass
        
    prompt = f"""
[START OF KNOWLEDGE BASE CONTEXT]
{context_str}
[END OF KNOWLEDGE BASE CONTEXT]

USER QUESTION: {query}

INSTRUCTIONS:
1. ONLY use the data provided in the [START OF KNOWLEDGE BASE CONTEXT] block above.
2. If the answer is not in the context, say "I do not have enough data to answer that."
3. Do not mix data between different farms or blocks.
4. Respond with actionable advice and tag severity as [CRITICAL], [HIGH], [MEDIUM], or [LOW] if applicable.
"""

    sources = list(set([c.split('\n')[0] for c in contexts]))
    yield json.dumps({"type": "sources", "sources": sources}) + "\n"

    ollama_url = f"{config.OLLAMA_BASE_URL}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "system": system_prompt,
        "stream": True
    }
    
    try:
        async with httpx.AsyncClient(timeout=300.0) as client:
            async with client.stream("POST", ollama_url, json=payload) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if not line.strip(): continue
                    try:
                        data = json.loads(line)
                        chunk = data.get("response", "")
                        yield json.dumps({"type": "chunk", "text": chunk}) + "\n"
                    except json.JSONDecodeError:
                        continue
    except Exception as e:
        yield json.dumps({"type": "error", "text": f"\n\nError calling Ollama: {str(e)}"}) + "\n"

async def list_models():
    ollama_url = f"{config.OLLAMA_BASE_URL}/api/tags"
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(ollama_url)
            response.raise_for_status()
            data = response.json()
            return [model['name'] for model in data.get('models', [])]
    except Exception:
        return [config.OLLAMA_DEFAULT_MODEL]
