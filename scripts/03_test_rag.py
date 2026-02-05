#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from rag.embeddings import EmbeddingGenerator
from rag.vectorstore import AyurvedicVectorStore  
from rag.retriever import RAGRetriever

vectorstore = AyurvedicVectorStore()
embedding_gen = EmbeddingGenerator()
retriever = RAGRetriever(vectorstore, embedding_gen)

test_queries = [
    "What are Vata characteristics?",
    "How to treat digestive problems?",
    "Pitta imbalance symptoms"
]

for query in test_queries:
    print(f"\n{'='*70}\nQuery: {query}\n{'='*70}")
    results = retriever.retrieve(query, n_results=3)
    
    for i, chunk in enumerate(results, 1):
        print(f"\nResult {i}:")
        print(f"  Section: {chunk['metadata'].get('section', 'Unknown')}")
        print(f"  Preview: {chunk['text'][:150]}...")

print("\n✅ RAG test complete!")
