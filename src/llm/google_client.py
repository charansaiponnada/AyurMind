"""
Google AI (Gemini) API Client
"""

import os
import google.generativeai as genai
from typing import Optional, List, Dict

class GoogleClient:
    """Client for Google AI (Gemini) API"""
    
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Google API key not found. "
                "Please set the GOOGLE_API_KEY environment variable in a .env file."
            )
        
        genai.configure(api_key=self.api_key)
        
        self.model_name = model or os.getenv("GOOGLE_MODEL", "gemini-1.5-flash")

    def _format_history(self, conversation_history: Optional[List[Dict]]) -> List[Dict]:
        """Formats history for the Gemini API, mapping roles."""
        if not conversation_history:
            return []
        
        formatted_history = []
        for turn in conversation_history:
            # Gemini uses 'model' for the assistant's role
            role = "model" if turn["role"] == "assistant" else turn["role"]
            formatted_history.append({
                "role": role,
                "parts": [{"text": turn["content"]}]
            })
        return formatted_history

    def generate(self, prompt: str, system_prompt: Optional[str] = None, 
                 temperature: float = 0.5, max_tokens: int = 2048, 
                 conversation_history: Optional[List[Dict]] = None, **kwargs) -> str:
        """Generate response from Gemini model."""
        
        try:
            model = genai.GenerativeModel(
                model_name=self.model_name,
                system_instruction=system_prompt
            )
            
            # The Gemini API expects the history to be managed externally and passed to start_chat
            # The last user message is the `prompt` parameter.
            history = self._format_history(conversation_history) if conversation_history else []
            chat = model.start_chat(history=history)

            generation_config = genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens
            )

            response = chat.send_message(prompt, generation_config=generation_config)
            
            return response.text

        except Exception as e:
            # Catching a broad exception to handle various API errors
            # and provide a user-friendly message.
            raise RuntimeError(f"Google AI API Error: {e}")

    def generate_with_context(self, query: str, context: str, 
                             system_prompt: str, temperature: float = 0.3, 
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
