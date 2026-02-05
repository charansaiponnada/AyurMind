#!/usr/bin/env python3
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from rag.embeddings import EmbeddingGenerator
from rag.vectorstore import AyurvedicVectorStore

chunks_file = Path("./data/processed/all_chunks.json")
if not chunks_file.exists():
    print("Run 01_scrape_data.py first!")
    exit(1)

with open(chunks_file, 'r') as f:
    chunks = json.load(f)

print(f"Loaded {len(chunks)} chunks")
print("Generating embeddings...")

embedding_gen = EmbeddingGenerator()
vectorstore = AyurvedicVectorStore()

texts = [chunk['text'] for chunk in chunks]
embeddings = embedding_gen.embed_batch(texts)

print("Adding to vector database...")
vectorstore.add_chunks(chunks, embeddings.tolist())

print(f"✅ Done! {vectorstore.get_stats()['total_chunks']} chunks in DB")
