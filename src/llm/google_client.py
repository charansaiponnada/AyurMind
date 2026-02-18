
    def generate_stream(self, prompt: str, system_prompt: Optional[str] = None, 
                 temperature: float = 0.5, max_tokens: int = 4000, 
                 conversation_history: Optional[List[Dict]] = None, **kwargs):
        """
        Generate response from Gemini model as a stream of text chunks.
        
        Args:
            prompt: The user's prompt/query
            system_prompt: System instruction for the model (optional)
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens to generate
            conversation_history: Previous conversation turns (optional)
            **kwargs: Additional arguments (ignored)
            
        Yields:
            Generated text chunks
            
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

            # Generate response as a stream
            response_stream = model.generate_content(
                formatted_history,
                generation_config=generation_config,
                stream=True
            )
            
            for chunk in response_stream:
                if chunk.text:
                    yield chunk.text

        except Exception as e:
            # In a stream, we might yield an error message
            yield f"Google AI API Error: {str(e)}"
