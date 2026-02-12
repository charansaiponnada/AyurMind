"""Vector Store - ChromaDB interface"""
import os
from pathlib import Path
from typing import List, Dict, Optional
import chromadb
from tqdm import tqdm

class AyurvedicVectorStore:
    def __init__(self, persist_directory: str = None):
        if persist_directory is None:
            persist_directory = os.getenv("VECTOR_DB_PATH", "./data/vectordb")
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        
        self.client = chromadb.PersistentClient(path=str(self.persist_directory))
        self.collection = self.client.get_or_create_collection(
            name="ayurvedic_texts",
            metadata={"description": "Charaka Samhita chunks"}
        )
    
    def add_chunks(self, chunks: List[Dict], embeddings: List[List[float]], batch_size: int = 100):
        for i in tqdm(range(0, len(chunks), batch_size), desc="Adding chunks"):
            batch_chunks = chunks[i:i+batch_size]
            batch_embeddings = embeddings[i:i+batch_size]
            
            ids = [f"chunk_{i+j}" for j in range(len(batch_chunks))]
            documents = [chunk['text'] for chunk in batch_chunks]
            metadatas = [chunk['metadata'] for chunk in batch_chunks]
            
            self.collection.add(ids=ids, documents=documents, embeddings=batch_embeddings, metadatas=metadatas)
    
    def search(self, query_embedding: List[float], n_results: int = 5, category_filter: Optional[str] = None, source_filter: Optional[str] = None) -> Dict:
        where_conditions = []
        if category_filter:
            where_conditions.append({"category": category_filter})
        
        if source_filter:
            # Match source_filter against 'section' or 'chapter' metadata fields
            # Assuming source_filter will be an exact match to a section/chapter name
            where_conditions.append({"$or": [{"section": source_filter}, {"chapter": source_filter}]})
        
        where_clause = None
        if where_conditions:
            if len(where_conditions) == 1:
                where_clause = where_conditions[0]
            else:
                where_clause = {"$and": where_conditions}
                
        return self.collection.query(query_embeddings=[query_embedding], n_results=n_results, where=where_clause)
    
    def get_stats(self) -> Dict:
        total_count = self.collection.count()
        return {'total_chunks': total_count, 'categories': {}}
