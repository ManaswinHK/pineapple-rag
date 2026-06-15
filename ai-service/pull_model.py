import httpx
import time
import sys
from config import OLLAMA_BASE_URL, OLLAMA_DEFAULT_MODEL

def wait_and_pull():
    print(f"Waiting for Ollama service at {OLLAMA_BASE_URL}...")
    
    # Wait for Ollama to be up
    for _ in range(30):
        try:
            res = httpx.get(OLLAMA_BASE_URL)
            if res.status_code == 200:
                print("Ollama is up!")
                break
        except httpx.RequestError:
            pass
        time.sleep(2)
    else:
        print("Failed to connect to Ollama.")
        sys.exit(1)

    print(f"Ensuring model '{OLLAMA_DEFAULT_MODEL}' is pulled...")
    
    # Check if model exists
    res = httpx.get(f"{OLLAMA_BASE_URL}/api/tags")
    if res.status_code == 200:
        models = [m['name'] for m in res.json().get('models', [])]
        # Some tags might just be 'llama3' without ':latest'
        if OLLAMA_DEFAULT_MODEL in models or f"{OLLAMA_DEFAULT_MODEL}:latest" in models:
            print(f"Model '{OLLAMA_DEFAULT_MODEL}' already exists. Skipping pull.")
            return

    # Pull the model
    print(f"Pulling '{OLLAMA_DEFAULT_MODEL}'. This may take a few minutes (approx 4.7GB)...")
    with httpx.stream("POST", f"{OLLAMA_BASE_URL}/api/pull", json={"name": OLLAMA_DEFAULT_MODEL}, timeout=600.0) as r:
        if r.status_code != 200:
            print(f"Error pulling model: {r.read().decode('utf-8')}")
            sys.exit(1)
            
        for chunk in r.iter_text():
            if chunk.strip():
                print(chunk.strip())
            
    print(f"Successfully pulled {OLLAMA_DEFAULT_MODEL}!")

if __name__ == "__main__":
    wait_and_pull()
