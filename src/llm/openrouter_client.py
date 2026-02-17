"""
OpenRouter API Client

Uses OpenRouter's models for RAG-based generation.
Get API key: https://openrouter.ai/keys
"""

import os
import requests
from typing import Optional, List, Dict

class OpenRouterClient:
    """Client for OpenRouter API"""
    
    def __init__(self, api_key: str = None, model: str = None, base_url: str = "https://openrouter.ai/api/v1"):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenRouter API key not found. "
                "Please set the OPENROUTER_API_KEY environment variable in a .env file. "
                "You can get a free key at: https://openrouter.ai/keys"
            )
        
        self.model = model or os.getenv("DEFAULT_MODEL", "mistralai/mistral-7b-instruct:free")
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/charansaiponnada/AyurMind", # Required by OpenRouter for free models
            "X-Title": "AyurMind" # Required by OpenRouter
        }
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None, 
                 temperature: float = 0.3, max_tokens: int = 1500, 
                 conversation_history: Optional[List[Dict]] = None, **kwargs) -> str:
        """Generate response from LLM using OpenRouter's chat completions endpoint."""
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        if conversation_history:
            # Add all but the last user message from history
            for turn in conversation_history[:-1]:
                messages.append(turn)
        
        # Add the current user prompt
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
                timeout=180  # 3 minute timeout
            )
            response.raise_for_status() # Raises HTTPError for bad responses (4xx or 5xx)
            
            result = response.json()
            return result['choices'][0]['message']['content']
            
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code
            if status_code == 401:
                raise RuntimeError("OpenRouter API Error: Invalid API Key. Please check your OPENROUTER_API_KEY.")
            elif status_code == 402:
                raise RuntimeError("OpenRouter API Error: You have exceeded your free tier limit or credits.")
            elif status_code == 404:
                raise RuntimeError(f"OpenRouter API Error: Model '{self.model}' not found. Please check the model name.")
            else:
                raise RuntimeError(f"OpenRouter API Error: Received status code {status_code}. Response: {e.response.text}")
        except requests.exceptions.Timeout:
            raise RuntimeError("OpenRouter API Error: The request timed out. The model may be taking too long to respond.")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"OpenRouter API Error: A network error occurred: {e}")
    
    def generate_with_context(self, query: str, context: str, 
                             system_prompt: str, temperature: float = 0.3, 
                             max_tokens: int = 1500, conversation_history: Optional[List[Dict]] = None) -> str:
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
            max_tokens=max_tokens,
            conversation_history=conversation_history
        )