"""Treatment Agent - Personalized recommendations"""
from .base_agent import BaseAgent
from typing import Optional

class TreatmentAgent(BaseAgent):
    def __init__(self, rag_retriever, llm_client):
        super().__init__(name="Treatment Recommender", rag_retriever=rag_retriever, llm_client=llm_client, temperature=0.4)
    
    def get_system_prompt(self) -> str:
        return """You are an Ayurvedic therapist providing treatment recommendations. Suggest diet, herbs, lifestyle changes based on classical texts. Format: 1. Dietary Recommendations 2. Herbal Recommendations 3. Lifestyle Modifications 4. Therapeutic Practices 5. Important Notes"""
    
    def get_category_filter(self) -> Optional[str]:
        return "treatment"
