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
        # This regex looks for patterns like "(from/in) [Word] Sthana" or "[Word] Samhita"
        match = re.search(r"(?:from|in)\s+((?:\w+\s+)?(?:Sthana|Samhita|Kalpa))", query, re.IGNORECASE)
        if match:
            return match.group(1)
        # A simpler check if the above fails
        if "siddhi sthana" in query.lower():
            return "Siddhi Sthana"
        if "kalpa sthana" in query.lower():
            return "Kalpa Sthana"
        return None

    def analyze_query(self, query: str) -> Dict:
        query_lower = query.lower()
        needs_prakriti = any(term in query_lower for term in ['constitution', 'prakriti', 'vata', 'pitta', 'kapha', 'body type'])
        needs_dosha = any(term in query_lower for term in ['symptom', 'problem', 'pain', 'disorder', 'disease', 'sick', 'imbalance'])
        needs_treatment = any(term in query_lower for term in ['treatment', 'remedy', 'cure', 'help', 'diet', 'food', 'herb', 'medicine'])
        
        # This no longer defaults to activating all agents. If no keywords match,
        # it correctly signals a general, non-Ayurvedic query.
        return {'prakriti': needs_prakriti, 'dosha': needs_dosha, 'treatment': needs_treatment}

    def process_query(self, query: str, agent_activation: Dict, conversation_history: List[Dict] = None) -> Dict:
        """
        Processes the query by activating the necessary specialist agents and synthesizing their findings.
        This is the "slow path" for complex Ayurvedic queries.
        """
        results = {}
        requested_source = self._extract_requested_sources(query)
        
        if agent_activation['prakriti']:
            prakriti_result = self.prakriti_agent.process(query, conversation_history=conversation_history)
            results['prakriti'] = prakriti_result['response']
        
        if agent_activation['dosha']:
            additional_info = {'Prakriti Assessment': results['prakriti']} if 'prakriti' in results else {}
            dosha_result = self.dosha_agent.process(query, additional_info, conversation_history)
            results['dosha'] = dosha_result['response']
        
        if agent_activation['treatment']:
            additional_info = {}
            if 'prakriti' in results:
                additional_info['Prakriti'] = results['prakriti']
            if 'dosha' in results:
                additional_info['Dosha Imbalance'] = results['dosha']
            if requested_source:
                additional_info['Requested Source'] = requested_source
            
            treatment_result = self.treatment_agent.process(query, additional_info, conversation_history)
            results['treatment'] = treatment_result['response']
        
        synthesized_response = self.synthesize_response(query, results, conversation_history)
        
        return {'query': query, 'agent_responses': results, 'final_response': synthesized_response, 'agent_activation': agent_activation}
    
    def synthesize_response(self, query: str, agent_results: Dict, conversation_history: List[Dict] = None) -> str:
        synthesis_context = "Agent Analyses:\n\n"
        
        if 'prakriti' in agent_results:
            synthesis_context += f"CONSTITUTIONAL ASSESSMENT:\n{agent_results['prakriti']}\n\n"
        if 'dosha' in agent_results:
            synthesis_context += f"IMBALANCE ANALYSIS:\n{agent_results['dosha']}\n\n"
        if 'treatment' in agent_results:
            synthesis_context += f"TREATMENT RECOMMENDATIONS:\n{agent_results['treatment']}\n\n"
        
        system_prompt = """You are the head consultant at an Ayurvedic clinic, responsible for reviewing and synthesizing the analyses from your junior diagnosticians and therapists into a single, cohesive, and accurate report for the client.

**Your Final Review Checklist:**
1.  **Clinical Consistency**: Cross-reference the diagnosis with the recommended diet. If the diagnosis is 'Kapha', the diet MUST NOT contain Kapha-aggravating foods like milk, sweet fruits, or heavy grains. The recommendations must be consistent and logical.
2.  **Textual Accuracy**: Ensure that if the user requested a specific source (e.g., 'Kalpa Sthana'), the recommendations are genuinely from that source as described in the agent's analysis.
3.  **Clarity and Compassion**: Frame the final report in a clear, unified, and compassionate tone. Remove any redundant or contradictory information.

Synthesize the agent analyses into a final, polished, and verified consultation report."""
        
        synthesis_prompt = f"""The following are the analyses from your junior agents based on the user's query.\n\n{synthesis_context}\n\nPlease perform your final review and synthesize these into a single, cohesive, and accurate consultation response for the client."""
        
        return self.llm_client.generate(prompt=synthesis_prompt, system_prompt=system_prompt, temperature=self.temperature, max_tokens=1200, conversation_history=conversation_history)
    
    def simple_query(self, query: str, conversation_history: List[Dict] = None) -> str:
        """
        Analyzes the query and routes it to either the fast-path (general query)
        or the slow-path (Ayurvedic query).
        """
        agent_activation = self.analyze_query(query)
        is_ayurvedic_query = any(agent_activation.values())

        if is_ayurvedic_query:
            # SLOW PATH: Use the full multi-agent process for Ayurvedic questions.
            result = self.process_query(query, agent_activation, conversation_history)
            return result['final_response']
        else:
            # FAST PATH: Bypass agents for a direct, quick answer to general questions.
            system_prompt = "You are a helpful general assistant. Provide a concise and direct answer. If you are asked about Ayurveda, gently state that you can answer those questions in more detail if the user asks a more specific question about symptoms, constitution, or treatments."
            return self.llm_client.generate(
                prompt=query, 
                system_prompt=system_prompt,
                # Use a slightly higher temperature for more natural general conversation
                temperature=0.4, 
                max_tokens=1000,
                conversation_history=conversation_history
            )
