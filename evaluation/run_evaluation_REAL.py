"""
Real AyurMind Evaluation Script
Uses actual multi-agent RAG system for evaluation
"""

import csv
import json
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.rag.embeddings import EmbeddingGenerator
from src.rag.vectorstore import AyurvedicVectorStore
from src.rag.retriever import RAGRetriever
from src.llm.local_client import OllamaClient
from src.agents.prakriti_agent import PrakritiAgent
from src.agents.dosha_agent import DoshaAgent
from src.agents.treatment_agent import TreatmentAgent
from src.agents.orchestrator import OrchestratorAgent

load_dotenv()

print("="*70)
print(" AYURMIND REAL EVALUATION")
print("="*70)
print()

# Initialize AyurMind system
print("Initializing AyurMind system...")
vectorstore = AyurvedicVectorStore()
embedding_generator = EmbeddingGenerator()
retriever = RAGRetriever(vectorstore, embedding_generator)
llm_client = OllamaClient()

prakriti_agent = PrakritiAgent(retriever, llm_client)
dosha_agent = DoshaAgent(retriever, llm_client)
treatment_agent = TreatmentAgent(retriever, llm_client)
orchestrator = OrchestratorAgent(prakriti_agent, dosha_agent, treatment_agent, llm_client)

print("✓ AyurMind initialized\n")

def run_vanilla_llm(scenario):
    """
    Vanilla LLM without RAG or context
    """
    system_prompt = "You are a helpful assistant. Answer briefly about Ayurvedic health questions."
    
    try:
        response = llm_client.generate(
            prompt=scenario,
            system_prompt=system_prompt,
            temperature=0.7
        )
        
        # Try to extract prakriti if mentioned
        prakriti = "Unknown"
        for dosha in ["Vata", "Pitta", "Kapha"]:
            if dosha.lower() in response.lower():
                prakriti = dosha
                break
        
        return {
            "response": response,
            "prakriti": prakriti,
            "sources": [],
            "retrieved_context": ""
        }
    except Exception as e:
        return {
            "response": f"Error: {str(e)}",
            "prakriti": "Unknown",
            "sources": [],
            "retrieved_context": ""
        }

def run_single_agent_rag(scenario):
    """
    Single-agent RAG (no specialized agents)
    """
    system_prompt = """You are an Ayurvedic expert. Use the provided context from classical texts to answer questions.
Be specific and cite your sources."""
    
    try:
        # Get context
        chunks = retriever.retrieve(scenario, n_results=3)
        context = "\n\n".join([c['text'] for c in chunks])
        sources = [f"{c['metadata'].get('section', 'Unknown')} - {c['metadata'].get('chapter', 'Unknown')}" 
                  for c in chunks]
        
        # Generate response
        prompt = f"""Context from Ayurvedic texts:
{context}

Question: {scenario}

Provide a clear answer based on the context above."""
        
        response = llm_client.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.3
        )
        
        # Extract prakriti
        prakriti = "Unknown"
        for dosha in ["Vata", "Pitta", "Kapha"]:
            if dosha.lower() in response.lower():
                prakriti = dosha
                break
        
        return {
            "response": response,
            "prakriti": prakriti,
            "sources": sources,
            "retrieved_context": context[:500]  # First 500 chars
        }
    except Exception as e:
        return {
            "response": f"Error: {str(e)}",
            "prakriti": "Unknown",
            "sources": [],
            "retrieved_context": ""
        }

def run_ayurmind(scenario):
    """
    Full multi-agent AyurMind system
    """
    try:
        # Process through orchestrator
        result = orchestrator.process_query(scenario)
        
        # Extract prakriti from agent responses
        prakriti = "Unknown"
        if 'prakriti' in result.get('agent_responses', {}):
            prakriti_text = result['agent_responses']['prakriti']
            for dosha in ["Vata", "Pitta", "Kapha"]:
                if dosha in prakriti_text:
                    prakriti = dosha
                    break
        
        # Get sources from context
        chunks = retriever.retrieve(scenario, n_results=3)
        sources = [f"{c['metadata'].get('section', 'Unknown')} - {c['metadata'].get('chapter', 'Unknown')}" 
                  for c in chunks]
        context = "\n\n".join([c['text'][:200] for c in chunks])  # First 200 chars of each
        
        return {
            "response": result['final_response'],
            "prakriti": prakriti,
            "sources": sources,
            "retrieved_context": context,
            "agent_responses": result.get('agent_responses', {}),
            "processing_time": result.get('processing_time', 0)
        }
    except Exception as e:
        return {
            "response": f"Error: {str(e)}",
            "prakriti": "Unknown",
            "sources": [],
            "retrieved_context": "",
            "agent_responses": {},
            "processing_time": 0
        }

def run_evaluation():
    """
    Main evaluation pipeline
    """
    dataset_path = os.path.join('dataset', 'evaluation_cases.csv')
    results_dir = 'results'
    
    os.makedirs(results_dir, exist_ok=True)
    
    models = {
        "vanilla_llm": run_vanilla_llm,
        "single_agent_rag": run_single_agent_rag,
        "ayurmind": run_ayurmind
    }
    
    # Load test cases
    with open(dataset_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        test_cases = list(reader)
    
    print(f"Loaded {len(test_cases)} test cases\n")
    
    # Run each model
    for model_name, model_func in models.items():
        print("="*70)
        print(f" EVALUATING: {model_name.upper()}")
        print("="*70)
        
        result_path = os.path.join(results_dir, f'results_{model_name}.jsonl')
        
        # Clear previous results
        if os.path.exists(result_path):
            os.remove(result_path)
        
        for i, case in enumerate(test_cases, 1):
            print(f"\n[{i}/{len(test_cases)}] Processing: {case['scenario'][:60]}...")
            
            # Get model output
            model_output = model_func(case['scenario'])
            
            # Prepare result
            result = {
                "case_id": case['id'],
                "scenario": case['scenario'],
                "ground_truth_prakriti": case.get('ground_truth_prakriti', 'Unknown'),
                "response": model_output["response"],
                "predicted_prakriti": model_output["prakriti"],
                "sources": model_output.get("sources", []),
                "retrieved_context": model_output.get("retrieved_context", "")
            }
            
            # Add agent responses for AyurMind
            if model_name == "ayurmind":
                result["agent_responses"] = model_output.get("agent_responses", {})
                result["processing_time"] = model_output.get("processing_time", 0)
            
            # Save result
            with open(result_path, 'a', encoding='utf-8') as f_out:
                f_out.write(json.dumps(result, ensure_ascii=False) + '\n')
            
            print(f"  ✓ Predicted Prakriti: {model_output['prakriti']}")
            print(f"  ✓ Response length: {len(model_output['response'])} chars")
            if model_name == "ayurmind":
                print(f"  ✓ Processing time: {model_output.get('processing_time', 0):.1f}s")
    
    print("\n" + "="*70)
    print(" EVALUATION COMPLETE!")
    print("="*70)
    print(f"\nResults saved in '{results_dir}/' directory")
    print("\nNext steps:")
    print("1. Review results files (results_*.jsonl)")
    print("2. Run: python calculate_metrics.py")
    print("3. Export for human review")

def export_for_human_review():
    """
    Export results in CSV format for BAMS expert review
    """
    results_dir = 'results'
    output_file = 'outputs_for_human_review.csv'
    
    print("\nExporting results for human review...")
    
    # Load all results
    all_results = []
    
    for model in ["vanilla_llm", "single_agent_rag", "ayurmind"]:
        result_path = os.path.join(results_dir, f'results_{model}.jsonl')
        
        if os.path.exists(result_path):
            with open(result_path, 'r', encoding='utf-8') as f:
                for line in f:
                    data = json.loads(line)
                    all_results.append({
                        'case_id': data['case_id'],
                        'model': model,
                        'query': data['scenario'],
                        'ground_truth_prakriti': data.get('ground_truth_prakriti', ''),
                        'predicted_prakriti': data['predicted_prakriti'],
                        'response': data['response'],
                        'sources': '; '.join(data.get('sources', [])),
                        'treatment_relevance': '',  # To be filled by expert
                        'safety_score': '',  # To be filled by expert
                        'health_literacy': '',  # To be filled by expert
                        'notes': ''  # Expert comments
                    })
    
    # Write to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'case_id', 'model', 'query', 'ground_truth_prakriti', 
            'predicted_prakriti', 'response', 'sources',
            'treatment_relevance', 'safety_score', 'health_literacy', 'notes'
        ])
        writer.writeheader()
        writer.writerows(all_results)
    
    print(f"✓ Exported to: {output_file}")
    print(f"  Total entries: {len(all_results)}")
    print("\nReview columns:")
    print("  - treatment_relevance: Rate 1-5 (1=poor, 5=excellent)")
    print("  - safety_score: Rate 1-5 (1=unsafe, 5=very safe)")
    print("  - health_literacy: Rate 1-5 (1=too complex, 5=very clear)")
    print("  - notes: Any additional comments")

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Run evaluation
    run_evaluation()
    
    # Export for review
    export_for_human_review()
    
    print("\n✅ DONE! Ready for BAMS expert review.")