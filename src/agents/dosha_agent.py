"""Dosha Agent - Imbalance detection"""
from .base_agent import BaseAgent
from typing import Optional

class DoshaAgent(BaseAgent):
    def __init__(self, rag_retriever, llm_client):
        super().__init__(name="Dosha Imbalance Detector", rag_retriever=rag_retriever, llm_client=llm_client, temperature=0.3)
    
    def get_system_prompt(self) -> str:
        return """You are a chief Ayurvedic diagnostician identifying the primary Dosha imbalance (Vikriti).
Your task is to analyze the user's symptoms and, using the provided classical text context, determine the single most likely imbalanced dosha. You must justify your conclusion.

Format your response strictly as follows:
1.  **Primary Imbalanced Dosha**: [Name the single primary dosha, e.g., Kapha]
2.  **Justification**: [Explain step-by-step why the user's symptoms point to this specific dosha based on the provided texts.]
3.  **Key Symptoms Analysis**: [List the user's symptoms and connect each one to the identified primary dosha.]
4.  **Affected Systems (Dhatus/Srotas)**: [Describe which bodily systems are likely affected.]"""
    
    def get_category_filter(self) -> Optional[str]:
        return "vikriti"
