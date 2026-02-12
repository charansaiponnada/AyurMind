import json
import csv
import os

def jsonl_to_csv(jsonl_filepath, csv_filepath):
    """
    Converts a JSONL file to a CSV file.
    Assumes all JSON objects have the same keys for consistent CSV headers.
    """
    data = []
    with open(jsonl_filepath, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))

    if not data:
        print(f"No data found in {jsonl_filepath}. CSV file will not be created.")
        return

    # Use keys from the first dictionary as CSV headers
    fieldnames = data[0].keys()

    with open(csv_filepath, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    
    print(f"Successfully converted '{jsonl_filepath}' to '{csv_filepath}'")

if __name__ == '__main__':
    # Define input and output file paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    jsonl_input_path = os.path.join(script_dir, 'results', 'results_vanilla_llm_only.jsonl')
    csv_output_path = os.path.join(script_dir, 'results', 'results_vanilla_llm_only.csv')

    # Ensure the results directory exists
    os.makedirs(os.path.dirname(csv_output_path), exist_ok=True)

    jsonl_to_csv(jsonl_input_path, csv_output_path)