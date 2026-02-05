"""
Local Ollama Client - 100% Free, Unlimited
"""

import os
import requests
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OllamaClient:
    """Client for local Ollama LLM"""
    
    def __init__(self, model: str = None, base_url: str = "http://localhost:11434"):
        self.model = model or os.getenv("LOCAL_MODEL", "llama3.2:3b")
        self.base_url = base_url
        
        logger.info(f"Initializing Ollama client with model: {self.model}")
        
        if not self.is_available():
            logger.warning(
                "⚠️ Ollama not available! Make sure:\n"
                "1. Ollama is installed\n"
                "2. Ollama is running\n"
                f"3. Model is downloaded: ollama pull {self.model}"
            )
    
    def is_available(self) -> bool:
        """Check if Ollama is running"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None, 
                 temperature: float = 0.3, **kwargs) -> str:
        """Generate response from local LLM
        
        Note: max_tokens is ignored for Ollama (not supported)
        """
        
        # Remove max_tokens if present (Ollama doesn't support it)
        kwargs.pop('max_tokens', None)
        
        if not self.is_available():
            raise RuntimeError(
                "Ollama is not running!\n"
                "It should be running automatically. Check with: ollama list"
            )
        
        # Build the complete prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"
        else:
            full_prompt = prompt
        
        payload = {
            "model": self.model,
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": 800  # Ollama's equivalent to max_tokens
            }
        }
        
        try:
            logger.info(f"Generating with Ollama ({self.model})...")
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=180  # 3 minutes max
            )
            response.raise_for_status()
            
            result = response.json()
            generated = result.get('response', '')
            
            logger.info(f"✓ Generated {len(generated)} characters")
            return generated
            
        except requests.exceptions.Timeout:
            raise RuntimeError("Ollama generation timed out. Try a smaller model.")
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Ollama API error: {e}")
            raise RuntimeError(f"Ollama error: {e}")
    
    def generate_with_context(self, query: str, context: str, 
                             system_prompt: str, temperature: float = 0.3,
                             **kwargs) -> str:
        """Generate response with RAG context
        
        Note: max_tokens is ignored for Ollama (not supported)
        """
        
        # Remove max_tokens if present
        kwargs.pop('max_tokens', None)
        
        prompt = f"""Context from Ayurvedic texts:

{context}

---

User Query: {query}

Based on the context provided above, please provide a response."""
        
        return self.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=temperature,
            **kwargs
        )