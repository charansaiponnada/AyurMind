import sys
import os
import time

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Get the project root directory (one level up from 'evaluation')
project_root = os.path.abspath(os.path.join(script_dir, '..'))
# Add the project root to sys.path
sys.path.insert(0, project_root)

import csv
import json
from src.agents.orchestrator import OrchestratorAgent
from src.agents.prakriti_agent import PrakritiAgent
from src.agents.dosha_agent import DoshaAgent
from src.agents.treatment_agent import TreatmentAgent
from src.llm.local_client import OllamaClient
from src.rag.retriever import RAGRetriever

# --- Model Placeholder Functions ---
# In a real scenario, these would import and call the actual model inference functions.

def run_vanilla_llm(scenario):
    """
    Placeholder for the vanilla LLM.
    Returns a generic, non-RAG response.
    """
    # This function remains a placeholder for comparison.
    # In a real system, you might instantiate a simple LLM client here.
    return {
        "response": f"As a large language model, I can provide some general information. Based on your symptoms like '{scenario[:30]}...', it could be related to stress or diet. It is always best to consult a doctor.",
        "prakriti": "Unknown",
        "sources": []
    }

def run_single_agent_rag(scenario, rag_retriever, llm_client):
    """
    Simulates a single-agent RAG system.
    This is more realistic than the previous placeholder.
    """
    # Use RAGRetriever's build_context for the context string
    context = rag_retriever.build_context(query=scenario)
    # Use RAGRetriever's retrieve for sources
    raw_sources = rag_retriever.retrieve(query=scenario)
    sources = [s.get('id', 'Unknown') for s in raw_sources] # Extract IDs from raw sources

    system_prompt = "You are a helpful Ayurvedic assistant. Analyze the user's query and provide a response based *only* on the provided context."
    response = llm_client.generate_with_context(
        query=scenario,
        context=context,
        system_prompt=system_prompt,
        temperature=0.3,
        max_tokens=500
    )
    
    # Simplified extraction for the placeholder
    prakriti = "Unknown"
    if "Vata" in response: prakriti = "Vata"
    elif "Pitta" in response: prakriti = "Pitta"
    elif "Kapha" in response: prakriti = "Kapha"

    return {
        "response": response,
        "prakriti": prakriti, 
        "sources": sources
    }

def run_ayurmind(scenario, orchestrator):
    """
    Runs the full multi-agent AyurMind system using the orchestrator.
    """
    orchestrator_output = orchestrator.simple_query(scenario)
    
    response = orchestrator_output.get("final_response", "No response from AyurMind.")
    
    predicted_prakriti = "Unknown"
    if 'agent_responses' in orchestrator_output and 'prakriti' in orchestrator_output.get('agent_responses', {}):
        prakriti_text = orchestrator_output['agent_responses']['prakriti']
        # More robust parsing to find the most likely dosha
        prakriti_text_lower = prakriti_text.lower()
        if "vata-pitta" in prakriti_text_lower or "pitta-vata" in prakriti_text_lower:
            predicted_prakriti = "Vata-Pitta"
        elif "pitta-kapha" in prakriti_text_lower or "kapha-pitta" in prakriti_text_lower:
            predicted_prakriti = "Pitta-Kapha"
        elif "vata-kapha" in prakriti_text_lower or "kapha-vata" in prakriti_text_lower:
            predicted_prakriti = "Vata-Kapha"
        elif "tridosha" in prakriti_text_lower:
            predicted_prakriti = "Tridosha"
        elif "vata" in prakriti_text_lower:
            predicted_prakriti = "Vata"
        elif "pitta" in prakriti_text_lower:
            predicted_prakriti = "Pitta"
        elif "kapha" in prakriti_text_lower:
            predicted_prakriti = "Kapha"

    sources = [s.get('id', s.get('title', 'Unknown Source')) for s in orchestrator_output.get('retrieved_sources', [])]

    return {
        "response": response,
        "prakriti": predicted_prakriti,
        "sources": sources
    }

# --- Main Evaluation Logic ---

def run_evaluation():
    """
    Main function to run the evaluation pipeline.
    """
    print("Starting evaluation...")

    dataset_path = os.path.join('dataset', 'evaluation_cases.csv')
    results_dir = 'results'

    # Ensure results directory exists
    os.makedirs(results_dir, exist_ok=True)

    # --- Full System Initialization ---
    print("Initializing AyurMind system components...")
    llm_client = OllamaClient()
    rag_retriever = RAGRetriever()
    
    # Initialize all agents with required dependencies
    prakriti_agent = PrakritiAgent(rag_retriever=rag_retriever, llm_client=llm_client)
    dosha_agent = DoshaAgent(rag_retriever=rag_retriever, llm_client=llm_client)
    treatment_agent = TreatmentAgent(rag_retriever=rag_retriever, llm_client=llm_client)
    
    orchestrator = OrchestratorAgent(
        prakriti_agent=prakriti_agent,
        dosha_agent=dosha_agent,
        treatment_agent=treatment_agent,
        llm_client=llm_client
    )
    print("Initialization complete.")
    
    models = {
        "vanilla_llm": run_vanilla_llm,
        "single_agent_rag": lambda s: run_single_agent_rag(s, rag_retriever, llm_client),
        "ayurmind": lambda s: run_ayurmind(s, orchestrator)
    }

    # Clear previous results files
    for model_name in models.keys():
        result_path = os.path.join(results_dir, f'results_{model_name}.jsonl')
        if os.path.exists(result_path):
            os.remove(result_path)

    with open(dataset_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        test_cases = list(reader)

    for model_name, model_func in models.items():
        print(f"--- Running evaluation for: {model_name} ---")
        result_path = os.path.join(results_dir, f'results_{model_name}.jsonl')

        for case in test_cases:
            print(f"  Processing case ID: {case['id']}")
            
            try:
                # Get model output
                model_output = model_func(case['scenario'])
                
                # Prepare result object
                result = {
                    "case_id": case['id'],
                    "scenario": case['scenario'],
                    "ground_truth_prakriti": case['ground_truth_prakriti'],
                    "response": model_output.get("response", "N/A"),
                    "predicted_prakriti": model_output.get("prakriti", "Unknown"),
                    "sources": model_output.get("sources", [])
                }
            except Exception as e:
                print(f"    ERROR processing case {case['id']} for model {model_name}: {e}")
                result = {
                    "case_id": case['id'],
                    "scenario": case['scenario'],
                    "ground_truth_prakriti": case['ground_truth_prakriti'],
                    "response": f"ERROR: {e}",
                    "predicted_prakriti": "Error",
                    "sources": []
                }
            
            # Append result to JSONL file
            with open(result_path, 'a', encoding='utf-8') as f_out:
                f_out.write(json.dumps(result) + '\n')
    
    print("\nEvaluation finished successfully!")
    print(f"Results saved in the '{results_dir}' directory.")


if __name__ == '__main__':
    # Change directory to the script's location to ensure relative paths work
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    run_evaluation()
