"""Orchestrator - Coordinates all agents"""
import os
import re
from typing import Dict, List, Optional

class OrchestratorAgent:
    def __init__(self, prakriti_agent, dosha_agent, treatment_agent, llm_client):
        self.prakriti_agent = prakriti_agent
        self.dosha_agent = dosha_agent
        self.treatment_agent = treatment_agent
        self.llm_client = llm_client
        self.temperature = float(os.getenv("ORCHESTRATOR_TEMP", "0.2"))
    
    def _extract_requested_sources(self, query: str) -> Optional[str]:
        """Extracts requested sources like 'Siddhi Sthana' using regex."""
        match = re.search(r"(?:from|in)\s+((?:\w+\s+)?(?:Sthana|Samhita|Kalpa))", query, re.IGNORECASE)
        if match:
            return match.group(1)
        if "siddhi sthana" in query.lower(): return "Siddhi Sthana"
        if "kalpa sthana" in query.lower(): return "Kalpa Sthana"
        return None

    def analyze_query(self, query: str) -> Dict:
        query_lower = query.lower()
        needs_prakriti = any(term in query_lower for term in ['constitution', 'prakriti', 'vata', 'pitta', 'kapha', 'body type'])
        needs_dosha = any(term in query_lower for term in ['symptom', 'problem', 'pain', 'disorder', 'disease', 'sick', 'imbalance'])
        needs_treatment = any(term in query_lower for term in ['treatment', 'remedy', 'cure', 'help', 'diet', 'food', 'herb', 'medicine'])
        return {'prakriti': needs_prakriti, 'dosha': needs_dosha, 'treatment': needs_treatment}

    def _get_synthesis_prompts(self, agent_results: Dict, retrieved_sources: List[Dict], user_mode: str) -> (str, str):
        synthesis_context = "Agent Analyses:\n\n"
        if 'prakriti' in agent_results: synthesis_context += f"CONSTITUTIONAL ASSESSMENT:\n{agent_results['prakriti']}\n\n"
        if 'dosha' in agent_results: synthesis_context += f"IMBALANCE ANALYSIS:\n{agent_results['dosha']}\n\n"
        if 'treatment' in agent_results: synthesis_context += f"TREATMENT RECOMMENDATIONS:\n{agent_results['treatment']}\n\n"

        source_context = "The following sources from Ayurvedic texts were consulted by the agents:\n"
        for i, source in enumerate(retrieved_sources, 1):
            metadata = source.get('metadata', {})
            source_ref = f"{metadata.get('section', 'Unknown Section')} - {metadata.get('chapter', 'Unknown Chapter')}"
            source_context += f"- Source {i}: {source_ref}\n"

        expert_system_prompt = """You are AyurMind, a senior Vaidya (Ayurvedic Physician) and academic... [Content remains the same]"""
        intermediate_system_prompt = """You are AyurMind, an experienced Vaidya (Ayurvedic Physician) explaining a case... [Content remains the same]"""
        beginner_system_prompt = """You are AyurMind, a friendly, modern, and empathetic Ayurvedic guide... [Content remains the same]"""

        system_prompt = expert_system_prompt
        if user_mode == 'beginner': system_prompt = beginner_system_prompt
        elif user_mode == 'intermediate': system_prompt = intermediate_system_prompt

        synthesis_prompt = f"""The following are the analyses from your junior agents... [Content remains the same]

{synthesis_context}

{source_context}
"""
        return system_prompt, synthesis_prompt

    def synthesize_response(self, query: str, agent_results: Dict, retrieved_sources: List[Dict], conversation_history: List[Dict] = None, user_mode: str = 'expert') -> str:
        system_prompt, synthesis_prompt = self._get_synthesis_prompts(agent_results, retrieved_sources, user_mode)
        return self.llm_client.generate(prompt=synthesis_prompt, system_prompt=system_prompt, temperature=self.temperature, max_tokens=4000, conversation_history=conversation_history)

    def synthesize_response_stream(self, query: str, agent_results: Dict, retrieved_sources: List[Dict], conversation_history: List[Dict] = None, user_mode: str = 'expert'):
        system_prompt, synthesis_prompt = self._get_synthesis_prompts(agent_results, retrieved_sources, user_mode)
        yield from self.llm_client.generate_stream(prompt=synthesis_prompt, system_prompt=system_prompt, temperature=self.temperature, max_tokens=4000, conversation_history=conversation_history)

    def _process_agents(self, query: str, agent_activation: Dict, conversation_history: List[Dict] = None) -> (Dict, List[Dict]):
        results = {}
        retrieved_sources = []
        requested_source = self._extract_requested_sources(query)
        base_additional_info = {'source_filter': requested_source} if requested_source else {}

        if agent_activation['prakriti']:
            prakriti_result = self.prakriti_agent.process(query, base_additional_info.copy(), conversation_history=conversation_history)
            results['prakriti'] = prakriti_result['response']
            if 'sources' in prakriti_result: retrieved_sources.extend(prakriti_result['sources'])
        
        if agent_activation['dosha']:
            dosha_additional_info = base_additional_info.copy()
            if 'prakriti' in results: dosha_additional_info['Prakriti Assessment'] = results['prakriti']
            dosha_result = self.dosha_agent.process(query, dosha_additional_info, conversation_history)
            results['dosha'] = dosha_result['response']
            if 'sources' in dosha_result: retrieved_sources.extend(dosha_result['sources'])

        if agent_activation['treatment']:
            treatment_additional_info = base_additional_info.copy()
            if 'prakriti' in results: treatment_additional_info['Prakriti'] = results['prakriti']
            if 'dosha' in results: treatment_additional_info['Dosha Imbalance'] = results['dosha']
            treatment_result = self.treatment_agent.process(query, treatment_additional_info, conversation_history)
            results['treatment'] = treatment_result['response']
            if 'sources' in treatment_result: retrieved_sources.extend(treatment_result['sources'])
            
        unique_sources = list({s['id']: s for s in retrieved_sources}.values())
        return results, unique_sources

    def process_query(self, query: str, agent_activation: Dict, conversation_history: List[Dict] = None, user_mode: str = 'expert') -> Dict:
        results, unique_sources = self._process_agents(query, agent_activation, conversation_history)
        synthesized_response = self.synthesize_response(query, results, unique_sources, conversation_history, user_mode)
        return {'query': query, 'agent_responses': results, 'final_response': synthesized_response, 'retrieved_sources': unique_sources, 'agent_activation': agent_activation}

    def process_query_stream(self, query: str, agent_activation: Dict, conversation_history: List[Dict] = None, user_mode: str = 'expert'):
        results, unique_sources = self._process_agents(query, agent_activation, conversation_history)
        yield from self.synthesize_response_stream(query, results, unique_sources, conversation_history, user_mode)

    def simple_query(self, query: str, conversation_history: List[Dict] = None, user_mode: str = 'expert') -> Dict:
        agent_activation = self.analyze_query(query)
        if any(agent_activation.values()):
            return self.process_query(query, agent_activation, conversation_history, user_mode=user_mode)
        else:
            system_prompt = "You are AyurMind, a friendly and knowledgeable Ayurvedic assistant..."
            response = self.llm_client.generate(prompt=query, system_prompt=system_prompt, temperature=0.4, max_tokens=2000, conversation_history=conversation_history)
            return {'query': query, 'final_response': response, 'retrieved_sources': [], 'agent_activation': agent_activation}

    def simple_query_stream(self, query: str, conversation_history: List[Dict] = None, user_mode: str = 'expert'):
        agent_activation = self.analyze_query(query)
        if any(agent_activation.values()):
            yield from self.process_query_stream(query, agent_activation, conversation_history, user_mode=user_mode)
        else:
            system_prompt = "You are AyurMind, a friendly and knowledgeable Ayurvedic assistant..."
            yield from self.llm_client.generate_stream(prompt=query, system_prompt=system_prompt, temperature=0.4, max_tokens=2000, conversation_history=conversation_history)
