"""Local Ollama Client - Fallback"""
import os, requests
from typing import Optional

class OllamaClient:
    def __init__(self, model: str = None, base_url: str = "http://localhost:11434"):
        self.model = model or os.getenv("LOCAL_MODEL", "llama3")
        self.base_url = base_url
    
    def is_available(self) -> bool:
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None, temperature: float = 0.3, **kwargs) -> str:
        if not self.is_available():
            raise RuntimeError("Ollama is not running! Start it with: ollama serve")
        
        payload = {"model": self.model, "prompt": prompt, "stream": False, "options": {"temperature": temperature}}
        if system_prompt:
            payload["system"] = system_prompt
        
        response = requests.post(f"{self.base_url}/api/generate", json=payload, timeout=120)
        response.raise_for_status()
        return response.json()['response']
    
    def generate_with_context(self, query: str, context: str, system_prompt: str, temperature: float = 0.3) -> str:
        prompt = f"Context from Ayurvedic texts:\n\n{context}\n\n---\n\nUser Query: {query}\n\nBased on the context provided above, please provide a response."
        return self.generate(prompt=prompt, system_prompt=system_prompt, temperature=temperature)
