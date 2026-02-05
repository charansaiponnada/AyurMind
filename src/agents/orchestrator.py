"""Orchestrator - Coordinates all agents"""
import os
from typing import Dict, List

class OrchestratorAgent:
    def __init__(self, prakriti_agent, dosha_agent, treatment_agent, llm_client):
        self.prakriti_agent = prakriti_agent
        self.dosha_agent = dosha_agent
        self.treatment_agent = treatment_agent
        self.llm_client = llm_client
        self.temperature = float(os.getenv("ORCHESTRATOR_TEMP", "0.2"))
    
    def analyze_query(self, query: str) -> Dict:
        query_lower = query.lower()
        needs_prakriti = any(term in query_lower for term in ['constitution', 'prakriti', 'vata', 'pitta', 'kapha', 'body type'])
        needs_dosha = any(term in query_lower for term in ['symptom', 'problem', 'pain', 'disorder', 'disease', 'sick', 'imbalance'])
        needs_treatment = any(term in query_lower for term in ['treatment', 'remedy', 'cure', 'help', 'diet', 'food', 'herb', 'medicine'])
        
        if not (needs_prakriti or needs_dosha or needs_treatment):
            needs_prakriti = needs_dosha = needs_treatment = True
        
        return {'prakriti': needs_prakriti, 'dosha': needs_dosha, 'treatment': needs_treatment}
    
    def process_query(self, query: str, conversation_history: List[Dict] = None) -> Dict:
        agent_activation = self.analyze_query(query)
        results = {}
        
        if agent_activation['prakriti']:
            prakriti_result = self.prakriti_agent.process(query)
            results['prakriti'] = prakriti_result['response']
        
        if agent_activation['dosha']:
            additional_info = {'Prakriti Assessment': results['prakriti']} if 'prakriti' in results else {}
            dosha_result = self.dosha_agent.process(query, additional_info)
            results['dosha'] = dosha_result['response']
        
        if agent_activation['treatment']:
            additional_info = {}
            if 'prakriti' in results:
                additional_info['Prakriti'] = results['prakriti']
            if 'dosha' in results:
                additional_info['Dosha Imbalance'] = results['dosha']
            
            treatment_result = self.treatment_agent.process(query, additional_info)
            results['treatment'] = treatment_result['response']
        
        synthesized_response = self.synthesize_response(query, results)
        
        return {'query': query, 'agent_responses': results, 'final_response': synthesized_response, 'agent_activation': agent_activation}
    
    def synthesize_response(self, query: str, agent_results: Dict) -> str:
        synthesis_context = "Agent Analyses:\n\n"
        
        if 'prakriti' in agent_results:
            synthesis_context += f"CONSTITUTIONAL ASSESSMENT:\n{agent_results['prakriti']}\n\n"
        if 'dosha' in agent_results:
            synthesis_context += f"IMBALANCE ANALYSIS:\n{agent_results['dosha']}\n\n"
        if 'treatment' in agent_results:
            synthesis_context += f"TREATMENT RECOMMENDATIONS:\n{agent_results['treatment']}\n\n"
        
        system_prompt = """You are the Orchestrator synthesizing Ayurvedic consultation. Create a unified, holistic report. Keep it clear and compassionate."""
        
        synthesis_prompt = f"""Original Query: {query}\n\n{synthesis_context}\n\nPlease synthesize the above analyses into a cohesive consultation response."""
        
        return self.llm_client.generate(prompt=synthesis_prompt, system_prompt=system_prompt, temperature=self.temperature, max_tokens=1200)
    
    def simple_query(self, query: str) -> str:
        result = self.process_query(query)
        return result['final_response']
