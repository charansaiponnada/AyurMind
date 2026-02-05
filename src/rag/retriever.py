"""RAG Retriever - Semantic search"""
import os
from typing import List, Dict, Optional
from .embeddings import EmbeddingGenerator
from .vectorstore import AyurvedicVectorStore

class RAGRetriever:
    def __init__(self, vectorstore=None, embedding_generator=None):
        self.vectorstore = vectorstore or AyurvedicVectorStore()
        self.embedding_generator = embedding_generator or EmbeddingGenerator()
        self.max_chunks = int(os.getenv("MAX_CHUNKS_PER_QUERY", "5"))
    
    def retrieve(self, query: str, n_results: int = None, category_filter: Optional[str] = None) -> List[Dict]:
        if n_results is None:
            n_results = self.max_chunks
        
        query_embedding = self.embedding_generator.embed_text(query)
        results = self.vectorstore.search(query_embedding=query_embedding.tolist(), n_results=n_results, category_filter=category_filter)
        
        retrieved_chunks = []
        for i in range(len(results['ids'][0])):
            chunk = {
                'id': results['ids'][0][i],
                'text': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i] if 'distances' in results else None
            }
            retrieved_chunks.append(chunk)
        
        return retrieved_chunks
    
    def build_context(self, query: str, n_results: int = None, category_filter: Optional[str] = None, include_metadata: bool = True) -> str:
        chunks = self.retrieve(query, n_results, category_filter)
        context_parts = []
        
        for i, chunk in enumerate(chunks, 1):
            if include_metadata:
                metadata = chunk['metadata']
                source = f"[Source: {metadata.get('section', 'Unknown')} - {metadata.get('chapter', 'Unknown')}]"
                context_parts.append(f"--- Context {i} {source} ---")
            else:
                context_parts.append(f"--- Context {i} ---")
            
            context_parts.append(chunk['text'])
            context_parts.append("")
        
        return "\n".join(context_parts)
