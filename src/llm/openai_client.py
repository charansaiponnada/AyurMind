"""
OpenAI API Client
"""

import os
from openai import OpenAI
from typing import Optional, List, Dict

class OpenAIClient:
    """Client for OpenAI API"""
    
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not found. "
                "Please set the OPENAI_API_KEY environment variable in a .env file."
            )
        
        self.client = OpenAI(api_key=self.api_key)
        self.model_name = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    def generate(self, prompt: str, system_prompt: Optional[str] = None, 
                 temperature: float = 0.5, max_tokens: int = 2048, 
                 conversation_history: Optional[List[Dict]] = None, **kwargs) -> str:
        """Generate response from OpenAI model."""
        
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            if conversation_history:
                # Add previous conversation turns
                for turn in conversation_history:
                    messages.append({"role": turn["role"], "content": turn["content"]})
            
            # Add the current user prompt
            messages.append({"role": "user", "content": prompt})

            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            
            return response.choices[0].message.content

        except Exception as e:
            raise RuntimeError(f"OpenAI API Error: {e}")

    def generate_with_context(self, query: str, context: str, 
                             system_prompt: str, temperature: float = 0.5, 
                             max_tokens: int = 2048, conversation_history: Optional[List[Dict]] = None) -> str:
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
