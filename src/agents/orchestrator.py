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
        retrieved_sources = []
        requested_source = self._extract_requested_sources(query)
        
        
        # Prepare common additional info for all agents, including the source filter if present
        base_additional_info = {}
        if requested_source:
            base_additional_info['source_filter'] = requested_source
        
        if agent_activation['prakriti']:
            prakriti_result = self.prakriti_agent.process(query, base_additional_info.copy(), conversation_history=conversation_history)
            results['prakriti'] = prakriti_result['response']
            if 'sources' in prakriti_result:
                retrieved_sources.extend(prakriti_result['sources'])

        if agent_activation['dosha']:
            dosha_additional_info = base_additional_info.copy()
            if 'prakriti' in results:
                dosha_additional_info['Prakriti Assessment'] = results['prakriti']
            dosha_result = self.dosha_agent.process(query, dosha_additional_info, conversation_history)
            results['dosha'] = dosha_result['response']
            if 'sources' in dosha_result:
                retrieved_sources.extend(dosha_result['sources'])
        
        if agent_activation['treatment']:
            treatment_additional_info = base_additional_info.copy()
            if 'prakriti' in results:
                treatment_additional_info['Prakriti'] = results['prakriti']
            if 'dosha' in results:
                treatment_additional_info['Dosha Imbalance'] = results['dosha']
            
            treatment_result = self.treatment_agent.process(query, treatment_additional_info, conversation_history)
            results['treatment'] = treatment_result['response']
            if 'sources' in treatment_result:
                retrieved_sources.extend(treatment_result['sources'])

        # Remove duplicate sources based on 'id'
        unique_sources = list({s['id']: s for s in retrieved_sources}.values())
        
        synthesized_response = self.synthesize_response(query, results, unique_sources, conversation_history)
        
        return {'query': query, 'agent_responses': results, 'final_response': synthesized_response, 'retrieved_sources': unique_sources, 'agent_activation': agent_activation}
    
    def synthesize_response(self, query: str, agent_results: Dict, retrieved_sources: List[Dict], conversation_history: List[Dict] = None) -> str:
        synthesis_context = "Agent Analyses:\n\n"
        
        if 'prakriti' in agent_results:
            synthesis_context += f"CONSTITUTIONAL ASSESSMENT:\n{agent_results['prakriti']}\n\n"
        if 'dosha' in agent_results:
            synthesis_context += f"IMBALANCE ANALYSIS:\n{agent_results['dosha']}\n\n"
        if 'treatment' in agent_results:
            synthesis_context += f"TREATMENT RECOMMENDATIONS:\n{agent_results['treatment']}\n\n"

        # Format sources for the prompt
        source_context = "The following sources from Ayurvedic texts were consulted by the agents:\n"
        for i, source in enumerate(retrieved_sources, 1):
            metadata = source.get('metadata', {})
            source_ref = f"{metadata.get('section', 'Unknown Section')} - {metadata.get('chapter', 'Unknown Chapter')}"
            source_context += f"- Source {i}: {source_ref}\n"

        system_prompt = """You are AyurMind, a senior Vaidya (Ayurvedic Physician) and academic, responsible for reviewing and synthesizing the findings of your junior agents into a formal consultation report. The final output is intended for an audience of BAMS graduates, practitioners, and students.

**STYLE AND TONE:**
- **Academic and Clinical**: Your tone must be formal, scholarly, and authoritative.
- **Precision over Personability**: Prioritize clinical accuracy and detailed explanations over conversational pleasantries. Avoid "friendly" or "approachable" language. Do not use phrasings like "Let me explain..." or "Here's what I found...".
- **Structured and Formal**: The final output must be a well-structured report. Use clear headings, subheadings, and bullet points or numbered lists.
- **No Salutations or Sign-offs**: Do not include openings like "Dear Client" or closings like "Sincerely." The report should begin directly with the first section.

**BACKGROUND VERIFICATION (DO NOT print in output):**
Before synthesizing, you must perform a final clinical review of the agents' analyses. Silently verify the following:
1.  **Clinical Consistency (Yukti)**: Ensure the Vikriti (imbalance) analysis aligns logically with the Chikitsa (treatment) plan. For example, a diagnosis of 'Ama' accumulation must be followed by 'Deepana-Pachana' (digestive fire kindling and toxin-digesting) recommendations. A Kapha-dominant Vikriti should not have Kapha-aggravating foods (e.g., excessive Madhura Rasa) in the diet plan.
2.  **Textual Accuracy (Shastra)**: If the user or agents referenced a specific text (e.g., 'Siddhi Sthana'), confirm the final recommendations are consistent with the scope and content of that classical source.
3.  **Safety (Ahimsa)**: Double-check that all advanced procedures (Shodhana Chikitsa like Vamana/Virechana) include a clear and non-negotiable warning that they require direct supervision by a qualified professional.

**TASK:**
Synthesize the provided agent analyses into a single, cohesive, and formal consultation report. The report must be structured, using the following headings. You must generate content for all sections based on the agent inputs.

**1. PROVISIONAL DIAGNOSIS (NIDANA & VIKRITI VIJNANA)**
    *   **Prakriti**: [State the constitutional baseline, if assessed]
    *   **Vikriti**: [Detail the current imbalance, including dominant doshas, their gunas, and the Samprapti (pathogenesis). Mention affected Dhatus and Srotas]

**2. TREATMENT PROTOCOL (CHIKITSA KRAMA)**
    *   **Chikitsa Sutra**: [State the core treatment principle]
    *   **Shodhana Chikitsa (Purification)**: [Outline recommended procedures with all necessary safety warnings]
    *   **Shamana Chikitsa (Palliative Care)**:
        *   **Aushadha Yoga (Herbal Formulations)**: [List recommended classical formulations]
        *   **Eka Dravya (Single Herbs)**: [List recommended single herbs]

**3. DIETARY & LIFESTYLE GUIDANCE (PATHYA-APATHYA)**
    *   **Pathya (Beneficial Diet/Actions)**: [Provide a list of recommended foods and lifestyle changes with justification]
    *   **Apathya (To-Be-Avoided Diet/Actions)**: [Provide a list of foods and activities to avoid, with justification]

**4. CLINICAL SUMMARY**
    *   [Provide a brief, high-level summary suitable for a fellow practitioner, encapsulating the case]
"""
        
        synthesis_prompt = f"""The following are the analyses from your junior agents and the sources they consulted.

{synthesis_context}

{source_context}

Please perform your final review as instructed and then synthesize these into a single, cohesive, and impactful consultation response for the client."""
        
        return self.llm_client.generate(prompt=synthesis_prompt, system_prompt=system_prompt, temperature=self.temperature, max_tokens=4000, conversation_history=conversation_history)
    
    def simple_query(self, query: str, conversation_history: List[Dict] = None) -> Dict:
        """
        Analyzes the query and routes it to either the fast-path (general query)
        or the slow-path (Ayurvedic query). Returns the full result dictionary.
        """
        agent_activation = self.analyze_query(query)
        is_ayurvedic_query = any(agent_activation.values())

        if is_ayurvedic_query:
            # SLOW PATH: Use the full multi-agent process for Ayurvedic questions.
            return self.process_query(query, agent_activation, conversation_history)
        else:
            # FAST PATH: Bypass agents for a direct, quick answer to general questions.
            system_prompt = "You are AyurMind, a friendly and knowledgeable Ayurvedic assistant. Answer general questions conversationally and helpfully. If asked about Ayurveda in general terms, provide a brief overview and mention you can offer more detailed guidance on specific health questions, symptoms, constitutions, or treatments."
            response = self.llm_client.generate(
                prompt=query, 
                system_prompt=system_prompt,
                temperature=0.4, 
                max_tokens=2000,
                conversation_history=conversation_history
            )
            return {'query': query, 'final_response': response, 'retrieved_sources': [], 'agent_activation': agent_activation}
