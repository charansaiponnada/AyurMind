import json
import csv
import os

def convert_jsonl_to_csv():
    results_dir = 'evaluation/results'
    output_dir = 'evaluation'

    jsonl_files = {
        'ayurmind': os.path.join(results_dir, 'results_ayurmind.jsonl'),
        'single_agent_rag': os.path.join(results_dir, 'results_single_agent_rag.jsonl'),
        'vanilla_llm': os.path.join(results_dir, 'results_vanilla_llm.jsonl')
    }

    # Prepare data for human review CSV
    human_review_data = []
    human_review_headers = [
        'case_id', 'scenario', 'ground_truth_prakriti',
        'ayurmind_response', 'ayurmind_predicted_prakriti', 'ayurmind_sources',
        'single_agent_rag_response', 'single_agent_rag_predicted_prakriti', 'single_agent_rag_sources',
        'vanilla_llm_response', 'vanilla_llm_predicted_prakriti', 'vanilla_llm_sources'
    ]

    # Temporary storage to merge results by case_id
    merged_results = {}

    for model_name, file_path in jsonl_files.items():
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        record = json.loads(line)
                        case_id = record.get('case_id')
                        if case_id not in merged_results:
                            merged_results[case_id] = {
                                'case_id': case_id,
                                'scenario': record.get('scenario'),
                                'ground_truth_prakriti': record.get('ground_truth_prakriti')
                            }
                        
                        merged_results[case_id][f'{model_name}_response'] = record.get('response')
                        merged_results[case_id][f'{model_name}_predicted_prakriti'] = record.get('predicted_prakriti')
                        # Sources can be a list, join them for CSV
                        merged_results[case_id][f'{model_name}_sources'] = ', '.join(record.get('sources', []))
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON from {file_path}: {e} - Line: {line.strip()}")
        else:
            print(f"Warning: {file_path} not found.")

    # Convert merged results to list for CSV writer
    for case_id in sorted(merged_results.keys(), key=lambda x: int(x)): # Sort by case_id numerically
        human_review_data.append(merged_results[case_id])

    # Write human_review.csv
    human_review_csv_path = os.path.join(output_dir, 'human_review.csv')
    with open(human_review_csv_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=human_review_headers)
        writer.writeheader()
        for row in human_review_data:
            # Ensure all headers are present in the row dictionary to avoid KeyError
            for header in human_review_headers:
                if header not in row:
                    row[header] = ''
            writer.writerow(row)
    print(f"Generated {human_review_csv_path}")

    # Prepare data for hallucination check CSV
    hallucination_check_data = []
    hallucination_check_headers = ['case_id', 'scenario', 'model_name', 'response', 'sources']

    for model_name, file_path in jsonl_files.items():
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        record = json.loads(line)
                        hallucination_check_data.append({
                            'case_id': record.get('case_id'),
                            'scenario': record.get('scenario'),
                            'model_name': model_name,
                            'response': record.get('response'),
                            'sources': ', '.join(record.get('sources', []))
                        })
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON from {file_path}: {e} - Line: {line.strip()}")
        
    # Write hallucination_check.csv
    hallucination_check_csv_path = os.path.join(output_dir, 'hallucination_check.csv')
    with open(hallucination_check_csv_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=hallucination_check_headers)
        writer.writeheader()
        writer.writerows(hallucination_check_data)
    print(f"Generated {hallucination_check_csv_path}")


if __name__ == '__main__':
    # Ensure the script runs from the project root if it's placed in a subdirectory
    # This assumes the script is in 'evaluation/' and project root is one level up.
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root_from_script = os.path.abspath(os.path.join(current_dir, '..'))
    os.chdir(project_root_from_script)
    
    convert_jsonl_to_csv()
