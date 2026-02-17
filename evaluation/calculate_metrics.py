import json
import os
import csv
from collections import defaultdict

# --- Metric Calculation Functions ---

def calculate_prakriti_accuracy(results):
    """
    Calculates the Prakriti classification accuracy.
    """
    correct = 0
    total = len(results)
    if total == 0:
        return 0.0

    for result in results:
        # Simple case-insensitive comparison
        if result['predicted_prakriti'].lower() == result['ground_truth_prakriti'].lower():
            correct += 1
    
    return (correct / total) * 100

def calculate_response_completeness(results):
    """
    Calculates the response completeness score based on a checklist of keywords.
    This is a simplified implementation.
    """
    completeness_checklist = {
        'constitutional_assessment': ['prakriti', 'constitution'],
        'imbalance_diagnosis': ['vikriti', 'imbalance', 'aggravation'],
        'dietary_recommendations': ['diet', 'food', 'eat'],
        'lifestyle_modifications': ['lifestyle', 'routine', 'daily'],
        'herbal_remedies': ['herb', 'remedy'],
        'source_citations': ['source', 'charaka', 'sushruta', 'ashtanga'],
        'follow_up': ['follow-up', 'consult'],
        'safety_disclaimers': ['disclaimer', 'educational', 'consult a practitioner']
    }
    
    total_score = 0
    total_cases = len(results)
    if total_cases == 0:
        return 0.0

    for result in results:
        response_text = result['response'].lower()
        checked_items = 0
        for key, keywords in completeness_checklist.items():
            if any(keyword in response_text for keyword in keywords):
                checked_items += 1
        
        completeness_score = (checked_items / len(completeness_checklist)) * 100
        total_score += completeness_score
        
    return total_score / total_cases

# --- Human Review File Generation ---

def generate_human_review_files(model_results):
    """
    Generates CSV files for human experts to review and rate the model outputs.
    """
    print("\nGenerating files for human review...")
    
    # --- File for Relevance, Safety, Health Literacy, Interpretability ---
    review_header = [
        "case_id", "model", "scenario", "response", 
        "treatment_relevance_score (1-5)", "safety_score (0-5)", 
        "health_literacy_score (0-5)", "interpretability_score (0-5)"
    ]
    review_rows = []

    # --- File for Hallucination Check ---
    hallucination_header = ["case_id", "model", "statement", "is_grounded (yes/no)"]
    hallucination_rows = []

    for model_name, results in model_results.items():
        for result in results:
            # Add row for the main review file
            review_rows.append({
                "case_id": result['case_id'],
                "model": model_name,
                "scenario": result['scenario'],
                "response": result['response'],
                "treatment_relevance_score (1-5)": "",
                "safety_score (0-5)": "",
                "health_literacy_score (0-5)": "",
                "interpretability_score (0-5)": ""
            })

            # Add rows for hallucination check (split response into sentences)
            sentences = result['response'].split('.')
            for sentence in sentences:
                if sentence.strip():
                    hallucination_rows.append({
                        "case_id": result['case_id'],
                        "model": model_name,
                        "statement": sentence.strip(),
                        "is_grounded (yes/no)": ""
                    })

    # Write the CSV files
    with open('outputs_for_human_review.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=review_header)
        writer.writeheader()
        writer.writerows(review_rows)

    with open('outputs_for_hallucination_check.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=hallucination_header)
        writer.writeheader()
        writer.writerows(hallucination_rows)

    print("Successfully generated 'outputs_for_human_review.csv' and 'outputs_for_hallucination_check.csv'.")
    print("Please have experts fill in the rating columns in these files.")


# --- Main Calculation Logic ---

def calculate_metrics():
    """
    Main function to calculate all metrics.
    """
    print("Calculating metrics...")
    
    results_dir = 'results'
    if not os.path.exists(results_dir):
        print(f"Error: Results directory '{results_dir}' not found. Please run 'run_evaluation.py' first.")
        return

    model_results = defaultdict(list)
    
    # Load results from all .jsonl files in the results directory
    for filename in os.listdir(results_dir):
        if filename.endswith('.jsonl'):
            model_name = filename.replace('results_', '').replace('.jsonl', '')
            filepath = os.path.join(results_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    model_results[model_name].append(json.loads(line))

    # --- Calculate and Print Metrics ---
    print("\n--- Evaluation Results ---")
    
    summary = {}
    for model_name, results in model_results.items():
        print(f"\nModel: {model_name}")
        
        accuracy = calculate_prakriti_accuracy(results)
        completeness = calculate_response_completeness(results)
        
        summary[model_name] = {
            "prakriti_accuracy": accuracy,
            "response_completeness": completeness
        }
        
        print(f"  Prakriti Classification Accuracy: {accuracy:.2f}%")
        print(f"  Average Response Completeness: {completeness:.2f}%")
    
    # --- Generate files for human review ---
    generate_human_review_files(model_results)

    # --- Generate Markdown Report ---
    generate_markdown_report(summary)


def generate_markdown_report(summary):
    """
    Generates a markdown report summarizing the evaluation results.
    """
    print("\nGenerating markdown report...")

    report = """# AyurMind Evaluation Summary Report

This document summarizes the automated evaluation results for the AyurMind project.
Metrics requiring human review are marked as 'N/A' and can be calculated after a manual review of the generated CSV files.

## Comparative Performance

| METRIC                      | VANILLA LLM   | SINGLE-AGENT RAG | AYURMIND      |
|-----------------------------|---------------|------------------|---------------|
| **PRAKRITI ACCURACY (%)**     | {vanilla_llm_prakriti_accuracy:.2f}     | {single_agent_rag_prakriti_accuracy:.2f}       | {ayurmind_prakriti_accuracy:.2f}      |
| **RESPONSE COMPLETENESS (%)** | {vanilla_llm_response_completeness:.2f} | {single_agent_rag_response_completeness:.2f}     | {ayurmind_response_completeness:.2f}    |
| **TREATMENT RELEVANCE**     | N/A           | N/A              | N/A           |
| **HALLUCINATION RATE (%)**  | N/A           | N/A              | N/A           |
| **SAFETY SCORE**            | N/A           | N/A              | N/A           |
| **HEALTH LITERACY**         | N/A           | N/A              | N/A           |

*N/A: Not applicable for automated calculation. Requires human review.*
""".format(
        vanilla_llm_prakriti_accuracy=summary.get('vanilla_llm', {}).get('prakriti_accuracy', 0.0),
        single_agent_rag_prakriti_accuracy=summary.get('single_agent_rag', {}).get('prakriti_accuracy', 0.0),
        ayurmind_prakriti_accuracy=summary.get('ayurmind', {}).get('prakriti_accuracy', 0.0),
        vanilla_llm_response_completeness=summary.get('vanilla_llm', {}).get('response_completeness', 0.0),
        single_agent_rag_response_completeness=summary.get('single_agent_rag', {}).get('response_completeness', 0.0),
        ayurmind_response_completeness=summary.get('ayurmind', {}).get('response_completeness', 0.0)
    )

    with open('evaluation_summary_report.md', 'w', encoding='utf-8') as f:
        f.write(report)

    print("Successfully generated 'evaluation_summary_report.md'.")


    # Note: Hallucination rate, relevance scores, etc., can be calculated
    # in a separate script after the human review CSVs are filled out.

if __name__ == '__main__':
    # Change directory to the script's location to ensure relative paths work
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    calculate_metrics()
