"""
Google AI (Gemini) API Client
"""

import os
import google.generativeai as genai
from typing import Optional, List, Dict, Union

class GoogleClient:
    """Client for Google AI (Gemini) API"""
    
    def __init__(self, api_key: str = None, model: str = None):
        """
        Initialize the Google AI client.
        
        Args:
            api_key: Google API key (optional, will use GOOGLE_API_KEY env var if not provided)
            model: Model name (optional, defaults to gemini-1.5-flash)
        """
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Google API key not found. "
                "Please set the GOOGLE_API_KEY environment variable in a .env file."
            )
        
        genai.configure(api_key=self.api_key)
        
        self.model_name = model or os.getenv("GOOGLE_MODEL", "gemini-1.5-flash")

    def _extract_text_content(self, content: Union[str, List, Dict]) -> str:
        """
        Extract text content from various message formats.
        
        Args:
            content: Can be a string, dict with 'text' key, or list of dicts
            
        Returns:
            Extracted text as string
        """
        # If content is already a string, return it
        if isinstance(content, str):
            return content
        
        # If content is a list (Gradio format)
        if isinstance(content, list):
            text_parts = []
            for item in content:
                if isinstance(item, dict) and 'text' in item:
                    text_parts.append(item['text'])
                elif isinstance(item, str):
                    text_parts.append(item)
            return " ".join(text_parts)
        
        # If content is a dict with 'text' key
        if isinstance(content, dict) and 'text' in content:
            return content['text']
        
        # Fallback: convert to string
        return str(content)

    def _format_history(self, conversation_history: Optional[List[Dict]]) -> List[Dict]:
        """
        Formats history for the Gemini API, mapping roles.
        
        Args:
            conversation_history: List of conversation turns with 'role' and 'content' keys
            
        Returns:
            Formatted history for Gemini API
        """
        if not conversation_history:
            return []
        
        formatted_history = []
        for turn in conversation_history:
            # Gemini uses 'model' for the assistant's role, 'user' for user
            role = "model" if turn["role"] == "assistant" else "user"
            
            # Extract text content from the turn
            text_content = self._extract_text_content(turn["content"])
            
            # Pass content as string directly in parts array
            formatted_history.append({
                "role": role,
                "parts": [text_content]
            })
        return formatted_history

    def generate(self, prompt: str, system_prompt: Optional[str] = None, 
                 temperature: float = 0.5, max_tokens: int = 2048, 
                 conversation_history: Optional[List[Dict]] = None, **kwargs) -> str:
        """
        Generate response from Gemini model using the stateless generate_content method.
        
        Args:
            prompt: The user's prompt/query
            system_prompt: System instruction for the model (optional)
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens to generate
            conversation_history: Previous conversation turns (optional)
            **kwargs: Additional arguments (ignored)
            
        Returns:
            Generated text response
            
        Raises:
            RuntimeError: If API call fails
        """
        try:
            # Initialize model with system instruction
            model = genai.GenerativeModel(
                model_name=self.model_name,
                system_instruction=system_prompt
            )
            
            # Format the conversation history
            formatted_history = self._format_history(conversation_history) if conversation_history else []
            
            # Extract text from prompt (in case it's also in Gradio format)
            prompt_text = self._extract_text_content(prompt)
            
            # Add the current user prompt
            formatted_history.append({
                "role": "user",
                "parts": [prompt_text]
            })

            # Configure generation parameters
            generation_config = genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens
            )

            # Generate response
            response = model.generate_content(
                formatted_history,
                generation_config=generation_config,
                stream=False
            )
            
            # Check if response has text
            if not response.text:
                raise ValueError("Empty response from model")
            
            # Return the generated text
            return response.text

        except Exception as e:
            # Catch all exceptions and provide user-friendly error message
            raise RuntimeError(f"Google AI API Error: {str(e)}")

    def generate_with_context(self, query: str, context: str, 
                             system_prompt: str, temperature: float = 0.3, 
                             max_tokens: int = 2048, 
                             conversation_history: Optional[List[Dict]] = None) -> str:
        """
        Generate response with RAG (Retrieval Augmented Generation) context.
        
        Args:
            query: The user's query
            context: Retrieved context from knowledge base
            system_prompt: System instruction for the model
            temperature: Sampling temperature (default: 0.3 for more focused responses)
            max_tokens: Maximum tokens to generate
            conversation_history: Previous conversation turns (optional)
            
        Returns:
            Generated text response based on context
            
        Raises:
            RuntimeError: If API call fails
        """
        # Extract text from query (in case it's in Gradio format)
        query_text = self._extract_text_content(query)
        
        # Construct prompt with context
        prompt = f"""Context from Ayurvedic texts:

{context}

---

User Query: {query_text}

Based on the context provided above, please provide a response."""
        
        # Generate response using the main generate method
        return self.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            conversation_history=conversation_history
        )