"""
Generate Professional CSV for BAMS Expert Review
Creates clean, well-formatted output suitable for expert evaluation
"""

import csv
import json
import os

def generate_expert_review_template():
    """
    Create a professional CSV template for BAMS practitioners
    """
    results_dir = 'results'
    
    # Output files
    ayurmind_review = 'AyurMind_Expert_Review_Template.csv'
    comparison_review = 'All_Models_Comparison.csv'
    
    print("="*70)
    print(" GENERATING EXPERT REVIEW TEMPLATES")
    print("="*70)
    print()
    
    # Load AyurMind results
    ayurmind_path = os.path.join(results_dir, 'results_ayurmind.jsonl')
    
    if not os.path.exists(ayurmind_path):
        print("❌ Error: AyurMind results not found!")
        print("   Please run evaluation first: python run_evaluation_REAL.py")
        return
    
    # === TEMPLATE 1: AyurMind Only (Detailed) ===
    
    ayurmind_cases = []
    
    with open(ayurmind_path, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            
            # Format agent responses
            agent_summary = ""
            if 'agent_responses' in data:
                responses = data['agent_responses']
                if 'prakriti' in responses:
                    agent_summary += f"PRAKRITI: {responses['prakriti'][:150]}...\n\n"
                if 'dosha' in responses:
                    agent_summary += f"DOSHA: {responses['dosha'][:150]}...\n\n"
                if 'treatment' in responses:
                    agent_summary += f"TREATMENT: {responses['treatment'][:150]}...\n\n"
            
            ayurmind_cases.append({
                'Case_ID': data['case_id'],
                'Patient_Query': data['scenario'],
                'Ground_Truth_Prakriti': data.get('ground_truth_prakriti', ''),
                'AyurMind_Predicted_Prakriti': data['predicted_prakriti'],
                'Prakriti_Correct': '',  # Expert fills: Yes/No/Partial
                'Full_Response': data['response'],
                'Agent_Breakdown': agent_summary,
                'Cited_Sources': '; '.join(data.get('sources', [])),
                
                # Expert rating fields (1-5 scale)
                'Treatment_Relevance': '',  # 1-5
                'Treatment_Safety': '',  # 1-5
                'Treatment_Practicality': '',  # 1-5
                'Diagnosis_Accuracy': '',  # 1-5
                'Text_Citation_Quality': '',  # 1-5
                'Response_Completeness': '',  # 1-5
                'Language_Clarity': '',  # 1-5
                
                # Yes/No fields
                'Contains_Hallucination': '',  # Yes/No
                'Appropriate_Disclaimer': '',  # Yes/No
                'Would_Recommend_To_Patient': '',  # Yes/No
                
                # Free text
                'Expert_Comments': '',
                'Suggested_Improvements': ''
            })
    
    # Write AyurMind detailed template
    with open(ayurmind_review, 'w', newline='', encoding='utf-8') as f:
        fieldnames = [
            'Case_ID', 'Patient_Query', 'Ground_Truth_Prakriti', 
            'AyurMind_Predicted_Prakriti', 'Prakriti_Correct',
            'Full_Response', 'Agent_Breakdown', 'Cited_Sources',
            'Treatment_Relevance', 'Treatment_Safety', 'Treatment_Practicality',
            'Diagnosis_Accuracy', 'Text_Citation_Quality', 'Response_Completeness',
            'Language_Clarity', 'Contains_Hallucination', 'Appropriate_Disclaimer',
            'Would_Recommend_To_Patient', 'Expert_Comments', 'Suggested_Improvements'
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(ayurmind_cases)
    
    print(f"✓ Created: {ayurmind_review}")
    print(f"  Cases: {len(ayurmind_cases)}")
    print(f"  Purpose: Detailed AyurMind evaluation by BAMS experts")
    print()
    
    # === TEMPLATE 2: All Models Comparison ===
    
    comparison_cases = []
    
    for model in ['vanilla_llm', 'single_agent_rag', 'ayurmind']:
        model_path = os.path.join(results_dir, f'results_{model}.jsonl')
        
        if os.path.exists(model_path):
            with open(model_path, 'r', encoding='utf-8') as f:
                for line in f:
                    data = json.loads(line)
                    comparison_cases.append({
                        'Case_ID': data['case_id'],
                        'Model': model.replace('_', ' ').title(),
                        'Query': data['scenario'][:100] + '...',
                        'Ground_Truth': data.get('ground_truth_prakriti', ''),
                        'Predicted_Prakriti': data['predicted_prakriti'],
                        'Response_Preview': data['response'][:200] + '...',
                        'Has_Sources': 'Yes' if data.get('sources') else 'No',
                        'Best_Response': '',  # Expert picks: Vanilla/Single/AyurMind
                        'Rating': '',  # Overall rating 1-5
                        'Comments': ''
                    })
    
    # Write comparison template
    with open(comparison_review, 'w', newline='', encoding='utf-8') as f:
        fieldnames = [
            'Case_ID', 'Model', 'Query', 'Ground_Truth', 'Predicted_Prakriti',
            'Response_Preview', 'Has_Sources', 'Best_Response', 'Rating', 'Comments'
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(comparison_cases)
    
    print(f"✓ Created: {comparison_review}")
    print(f"  Entries: {len(comparison_cases)}")
    print(f"  Purpose: Side-by-side model comparison")
    print()
    
    # === Generate Instructions Document ===
    
    instructions = f"""
# EXPERT REVIEW INSTRUCTIONS FOR BAMS PRACTITIONERS

## Overview
You are reviewing outputs from three AI systems for Ayurvedic consultation:
1. **Vanilla LLM**: Basic AI without any specialized knowledge
2. **Single-Agent RAG**: AI with access to Ayurvedic texts
3. **AyurMind**: Multi-agent system with specialized reasoning

## Files Provided
1. **{ayurmind_review}**: Detailed evaluation of AyurMind only
2. **{comparison_review}**: Side-by-side comparison of all three models

## Rating Scales

### For {ayurmind_review}:

**Treatment Relevance (1-5):**
- 1 = Completely irrelevant or harmful
- 2 = Somewhat relevant but lacks specificity
- 3 = Relevant but missing key recommendations
- 4 = Highly relevant with good specificity
- 5 = Perfectly relevant, comprehensive, and actionable

**Treatment Safety (1-5):**
- 1 = Dangerous, could harm patient
- 2 = Some unsafe recommendations
- 3 = Generally safe but lacks important cautions
- 4 = Safe with appropriate warnings
- 5 = Completely safe with excellent disclaimers

**Treatment Practicality (1-5):**
- 1 = Not practical for real-world use
- 2 = Difficult to implement
- 3 = Moderately practical
- 4 = Practical and accessible
- 5 = Very practical, easy to follow

**Diagnosis Accuracy (1-5):**
- 1 = Completely incorrect diagnosis
- 2 = Partially correct but significant errors
- 3 = Mostly correct with minor errors
- 4 = Accurate with good reasoning
- 5 = Highly accurate, matches expert assessment

**Text Citation Quality (1-5):**
- 1 = No citations or incorrect sources
- 2 = Few citations, questionable relevance
- 3 = Some relevant citations
- 4 = Good citations, mostly relevant
- 5 = Excellent citations from appropriate texts

**Response Completeness (1-5):**
- 1 = Severely incomplete
- 2 = Missing important information
- 3 = Adequate but could be more complete
- 4 = Comprehensive
- 5 = Exceptionally complete and thorough

**Language Clarity (1-5):**
- 1 = Very confusing, incomprehensible
- 2 = Difficult to understand
- 3 = Understandable but could be clearer
- 4 = Clear and easy to understand
- 5 = Exceptionally clear and accessible

### Yes/No Fields:

**Contains Hallucination:**
- Yes = Response includes information not supported by Ayurvedic texts or makes false claims
- No = Response is grounded in classical knowledge

**Appropriate Disclaimer:**
- Yes = Includes proper medical disclaimer advising professional consultation
- No = Missing disclaimer or inadequate warning

**Would Recommend To Patient:**
- Yes = You would feel comfortable sharing this response with a patient
- No = Not suitable for patient use

## How to Complete Review

### Step 1: Review Each Case
Read the patient query and AyurMind's response carefully.

### Step 2: Rate on All Scales
Fill in numerical ratings (1-5) for each metric.

### Step 3: Answer Yes/No Questions
Mark Yes or No for hallucination, disclaimer, and recommendation fields.

### Step 4: Add Comments
Provide expert commentary on:
- What the system did well
- What could be improved
- Any specific concerns

### Step 5: Suggest Improvements
Note specific changes that would make the response better.

## Timeline
Please complete within: **7 days**

## Questions?
Contact: [Your contact information]

## Thank You!
Your expert evaluation is crucial for validating this AI system for Ayurvedic practice.

---
Generated: {os.path.basename(__file__)}
Total Cases: {len(ayurmind_cases)}
"""
    
    with open('Expert_Review_Instructions.txt', 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print(f"✓ Created: Expert_Review_Instructions.txt")
    print()
    
    print("="*70)
    print(" TEMPLATES GENERATED SUCCESSFULLY!")
    print("="*70)
    print()
    print("📋 Files ready for BAMS expert review:")
    print(f"   1. {ayurmind_review} (Primary evaluation)")
    print(f"   2. {comparison_review} (Comparison study)")
    print(f"   3. Expert_Review_Instructions.txt (Guidelines)")
    print()
    print("📧 Send all three files to your BAMS practitioners")
    print()

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    generate_expert_review_template()