"""Prakriti Agent - Constitutional assessment"""
from .base_agent import BaseAgent
from typing import Optional

class PrakritiAgent(BaseAgent):
    def __init__(self, rag_retriever, llm_client):
        super().__init__(name="Prakriti Assessor", rag_retriever=rag_retriever, llm_client=llm_client, temperature=0.3)
    
    def get_system_prompt(self) -> str:
        return """You are an expert Ayurvedic practitioner specializing in Prakriti assessment. Determine the user's Dosha (Vata/Pitta/Kapha) based on their traits. Format: 1. Constitutional Type 2. Confidence 3. Key Indicators 4. Explanation"""
    
    def get_category_filter(self) -> Optional[str]:
        return "prakriti"
