import csv
import json
import os

# --- Model Placeholder Functions ---
# In a real scenario, these would import and call the actual model inference functions.

def run_vanilla_llm(scenario):
    """
    Placeholder for the vanilla LLM.
    Returns a generic, non-RAG response.
    """
    return {
        "response": f"As a large language model, I can provide some general information. Based on your symptoms like '{scenario[:30]}...', it could be related to stress or diet. It is always best to consult a doctor.",
        "prakriti": "Unknown",
        "sources": []
    }

def run_single_agent_rag(scenario):
    """
    Placeholder for the single-agent RAG system.
    Returns a more specific response that mimics RAG but without specialized agents.
    """
    return {
        "response": f"Based on retrieved documents, your symptoms like '{scenario[:30]}...' may suggest an imbalance. Classical texts recommend certain lifestyle changes. [Source: Charaka Samhita, Sutra Sthana, Ch. 5]",
        "prakriti": "Vata-Pitta", # Example of a direct classification
        "sources": ["Charaka Samhita, Sutra Sthana, Ch. 5"]
    }

def run_ayurmind(scenario):
    """
    Placeholder for the full multi-agent AyurMind system.
    Returns a structured, multi-faceted response.
    """
    return {
        "response": """**Prakriti Assessment:** Your constitution appears to be predominantly Vata.
**Vikriti (Imbalance):** The symptoms you describe, such as anxiety and dryness, indicate a likely aggravation of Vata dosha.
**Recommendations:** To pacify Vata, consider incorporating warm, nourishing foods into your diet and establishing a regular daily routine. A gentle oil massage (Abhyanga) before bed can also be beneficial.
**Disclaimer:** This is educational information. Please consult a BAMS practitioner.""",
        "prakriti": "Vata",
        "sources": ["Charaka Samhita, Sutra Sthana, Ch. 12", "Ashtanga Hridaya, Sutra Sthana, Ch. 1"]
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

    models = {
        "vanilla_llm": run_vanilla_llm,
        "single_agent_rag": run_single_agent_rag,
        "ayurmind": run_ayurmind
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
            
            # Get model output
            model_output = model_func(case['scenario'])
            
            # Prepare result object
            result = {
                "case_id": case['id'],
                "scenario": case['scenario'],
                "ground_truth_prakriti": case['ground_truth_prakriti'],
                "response": model_output["response"],
                "predicted_prakriti": model_output["prakriti"],
                "sources": model_output["sources"]
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
