import sys
import os
import csv
import json

# Adjust sys.path to import modules from src
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.insert(0, project_root)

from src.llm.local_client import OllamaClient

def run_vanilla_llm(scenario, llm_client):
    """
    Instantiates a simple LLM client to generate a response based on the scenario.
    Provides a more informative, Ayurvedic-oriented response with a safety disclaimer.
    """
    system_prompt = (
        "You are an assistant knowledgeable in general Ayurvedic principles. "
        "Based on the user's symptoms, you can explain general Ayurvedic concepts "
        "or suggest potential dosha imbalances. Always include a disclaimer "
        "that this information is for educational purposes only and not a substitute "
        "for professional medical advice or diagnosis from a qualified Ayurvedic practitioner."
    )
    
    response = llm_client.generate(
        prompt=scenario,
        system_prompt=system_prompt,
        temperature=0.3,
        max_tokens=500
    )

    prakriti = "Unknown"
    response_lower = response.lower()
    if "vata-pitta" in response_lower or "pitta-vata" in response_lower:
        prakriti = "Vata-Pitta"
    elif "pitta-kapha" in response_lower or "kapha-pitta" in response_lower:
        prakriti = "Pitta-Kapha"
    elif "vata-kapha" in response_lower or "kapha-vata" in response_lower:
        prakriti = "Vata-Kapha"
    elif "tridosha" in response_lower:
        prakriti = "Tridosha"
    elif "vata" in response_lower:
        prakriti = "Vata"
    elif "pitta" in response_lower:
        prakriti = "Pitta"
    elif "kapha" in response_lower:
        prakriti = "Kapha"

    return {
        "response": response,
        "prakriti": prakriti,
        "sources": [] # Still no explicit sources for vanilla LLM
    }

def run_vanilla_only_evaluation():
    """
    Runs evaluation only for the vanilla LLM.
    """
    print("Starting vanilla LLM only evaluation...")

    dataset_path = os.path.join('dataset', 'evaluation_cases.csv')
    results_dir = 'results'

    # Ensure results directory exists
    os.makedirs(results_dir, exist_ok=True)

    print("Initializing OllamaClient...")
    llm_client = OllamaClient()
    print("OllamaClient initialized.")

    result_path = os.path.join(results_dir, 'results_vanilla_llm_only.jsonl')
    
    # Clear previous results file if it exists
    if os.path.exists(result_path):
        os.remove(result_path)

    with open(dataset_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        test_cases = list(reader)

    print(f"--- Running evaluation for: vanilla_llm_only ---")

    for case in test_cases:
        print(f"  Processing case ID: {case['id']}")
        
        try:
            # Get model output
            model_output = run_vanilla_llm(case['scenario'], llm_client)
            
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
            print(f"    ERROR processing case {case['id']} for vanilla_llm_only: {e}")
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
    
    print("\nVanilla LLM only evaluation finished successfully!")
    print(f"Results saved to '{result_path}'.")

if __name__ == '__main__':
    # Change directory to the script's location to ensure relative paths work
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    run_vanilla_only_evaluation()