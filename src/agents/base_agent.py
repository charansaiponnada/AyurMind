"""Base Agent - Foundation for specialists"""
from abc import ABC, abstractmethod
from typing import Dict, Optional

class BaseAgent(ABC):
    def __init__(self, name: str, rag_retriever, llm_client, temperature: float = 0.3, max_tokens: int = 800):
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
    
    def retrieve_context(self, query: str, n_results: int = 5) -> str:
        category_filter = self.get_category_filter()
        return self.rag_retriever.build_context(query=query, n_results=n_results, category_filter=category_filter, include_metadata=True)
    
    def generate_response(self, query: str, context: str = None, additional_info: Dict = None, conversation_history: list = None) -> str:
        if context is None:
            context = self.retrieve_context(query)
        
        if additional_info:
            info_str = "\n".join([f"{key}: {value}" for key, value in additional_info.items()])
            enhanced_query = f"{query}\n\nAdditional Information:\n{info_str}"
        else:
            enhanced_query = query
        
        return self.llm_client.generate_with_context(
            query=enhanced_query, context=context, system_prompt=self.get_system_prompt(),
            temperature=self.temperature, max_tokens=self.max_tokens,
            conversation_history=conversation_history
        )
    
    def process(self, query: str, additional_info: Dict = None, conversation_history: list = None) -> Dict:
        context = self.retrieve_context(query)
        response = self.generate_response(query, context, additional_info, conversation_history)
        return {'agent': self.name, 'response': response, 'context': context, 'query': query}
