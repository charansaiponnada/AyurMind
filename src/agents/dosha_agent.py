"""Dosha Agent - Imbalance detection"""
from .base_agent import BaseAgent
from typing import Optional

class DoshaAgent(BaseAgent):
    def __init__(self, rag_retriever, llm_client):
        super().__init__(name="Dosha Imbalance Detector", rag_retriever=rag_retriever, llm_client=llm_client, temperature=0.3)
    
    def get_system_prompt(self) -> str:
        return """You are an Ayurvedic diagnostician identifying Dosha imbalances (Vikriti). Analyze symptoms and correlate with classical texts. Format: 1. Imbalanced Dosha(s) 2. Severity 3. Affected Systems 4. Key Symptoms 5. Explanation"""
    
    def get_category_filter(self) -> Optional[str]:
        return "vikriti"
