"""
OpenRouter API Client - Free LLM access (FIXED)

Uses OpenRouter's free tier models for RAG-based generation.
Get free API key: https://openrouter.ai/keys
"""

import os
import requests
from typing import Optional

class OpenRouterClient:
    """Client for OpenRouter API"""
    
    def __init__(self, api_key: str = None, model: str = None, base_url: str = "https://openrouter.ai/api/v1"):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenRouter API key required! "
                "Set OPENROUTER_API_KEY in .env or pass to constructor. "
                "Get free key at: https://openrouter.ai/keys"
            )
        
        self.model = model or os.getenv("DEFAULT_MODEL", "meta-llama/llama-3.2-3b-instruct:free")
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/ayurmind",
            "X-Title": "AyurMind"
        }
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None, temperature: float = 0.3, max_tokens: int = 800, **kwargs) -> str:
        """Generate response from LLM"""
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            **kwargs
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            
            result = response.json()
            return result['choices'][0]['message']['content']
            
        except requests.exceptions.RequestException as e:
            print(f"OpenRouter API error: {e}")
            raise
    
    def generate_with_context(self, query: str, context: str, system_prompt: str, temperature: float = 0.3, max_tokens: int = 800) -> str:
        """Generate response with RAG context"""
        prompt = f"""Context from Ayurvedic texts:

{context}

---

User Query: {query}

Based on the context provided above, please provide a response."""
        
        return self.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens
        )