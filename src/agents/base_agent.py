"""Base Agent - Foundation for specialists"""
from abc import ABC, abstractmethod
from typing import Dict, Optional

class BaseAgent(ABC):
    def __init__(self, name: str, rag_retriever, llm_client, temperature: float = 0.3, max_tokens: int = 3000):
        self.name = name
        self.rag_retriever = rag_retriever
        self.llm_client = llm_client
        self.temperature = temperature
        self.max_tokens = max_tokens
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        pass
    
    @abstractmethod
    def get_category_filter(self) -> Optional[str]:
        pass
    
    def retrieve_context_and_sources(self, query: str, n_results: int = 5, source_filter: Optional[str] = None) -> (str, list):
        category_filter = self.get_category_filter()
        chunks = self.rag_retriever.retrieve(query=query, n_results=n_results, category_filter=category_filter, source_filter=source_filter)
        
        context_parts = []
        for i, chunk in enumerate(chunks, 1):
            metadata = chunk.get('metadata', {})
            source = f"[Source: {metadata.get('section', 'Unknown')} - {metadata.get('chapter', 'Unknown')}]"
            context_parts.append(f"--- Context {i} {source} ---")
            context_parts.append(chunk.get('text', ''))
            context_parts.append("")
        
        context_str = "\n".join(context_parts)
        return context_str, chunks

    def generate_response(self, query: str, context: str = None, additional_info: Dict = None, conversation_history: list = None) -> str:
        if context is None:
            # If context is not explicitly provided, retrieve it
            # Extract source_filter if available in additional_info
            _source_filter = additional_info.get('source_filter') if additional_info else None
            context, _ = self.retrieve_context_and_sources(query, source_filter=_source_filter)
        
        # Ensure 'source_filter' is not included in the LLM's additional_info if it's only for retrieval
        llm_additional_info = additional_info.copy() if additional_info else {}
        llm_additional_info.pop('source_filter', None) 
        
        if llm_additional_info:
            info_str = "\n".join([f"{key}: {value}" for key, value in llm_additional_info.items()])
            enhanced_query = f"{query}\n\nAdditional Information:\n{info_str}"
        else:
            enhanced_query = query
        
        return self.llm_client.generate_with_context(
            query=enhanced_query, context=context, system_prompt=self.get_system_prompt(),
            temperature=self.temperature, max_tokens=self.max_tokens,
            conversation_history=conversation_history
        )
    
    def process(self, query: str, additional_info: Dict = None, conversation_history: list = None) -> Dict:
        source_filter = additional_info.get('source_filter') if additional_info else None
        context, sources = self.retrieve_context_and_sources(query, source_filter=source_filter)
        response = self.generate_response(query, context, additional_info, conversation_history)
        return {'agent': self.name, 'response': response, 'sources': sources, 'query': query}
