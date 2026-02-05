"""Gradio Chat Interface"""
import os, sys
from pathlib import Path
import gradio as gr
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.rag.embeddings import EmbeddingGenerator
from src.rag.vectorstore import AyurvedicVectorStore
from src.rag.retriever import RAGRetriever
from src.llm.openrouter_client import OpenRouterClient
from src.llm.local_client import OllamaClient
from src.agents.prakriti_agent import PrakritiAgent
from src.agents.dosha_agent import DoshaAgent
from src.agents.treatment_agent import TreatmentAgent
from src.agents.orchestrator import OrchestratorAgent

load_dotenv()

class AyurMindApp:
    def __init__(self):
        self.vectorstore = AyurvedicVectorStore()
        self.embedding_generator = EmbeddingGenerator()
        self.retriever = RAGRetriever(self.vectorstore, self.embedding_generator)
        
        use_local = os.getenv("USE_LOCAL_FALLBACK", "false").lower() == "true"
        
        try:
            self.llm_client = OpenRouterClient()
        except:
            if use_local:
                self.llm_client = OllamaClient()
            else:
                raise
        
        self.prakriti_agent = PrakritiAgent(self.retriever, self.llm_client)
        self.dosha_agent = DoshaAgent(self.retriever, self.llm_client)
        self.treatment_agent = TreatmentAgent(self.retriever, self.llm_client)
        self.orchestrator = OrchestratorAgent(self.prakriti_agent, self.dosha_agent, self.treatment_agent, self.llm_client)
    
    def chat(self, message: str, history: list):
        if not message.strip():
            return "Please enter a question."
        
        try:
            response = self.orchestrator.simple_query(message)
            return response
        except Exception as e:
            return f"Error: {str(e)}. Please try again."
    
    def create_interface(self):
        with gr.Blocks(title="AyurMind") as interface:
            gr.HTML('<div style="text-align:center; padding:2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color:white; border-radius:10px;"><h1>🌿 AyurMind</h1><p style="font-size:1.2rem;">AI-Powered Ayurvedic Consultation</p></div>')
            
            gr.HTML('<div style="background:#fff3cd; border:1px solid #ffc107; padding:1rem; border-radius:5px; margin:1rem 0;"><strong>⚠️ Disclaimer:</strong> Educational only. Not medical advice. Consult professionals.</div>')
            
            chatbot = gr.Chatbot(height=500, label="Consultation")
            
            with gr.Row():
                msg = gr.Textbox(label="Your Question", placeholder="Describe your concern...", scale=4)
                submit = gr.Button("Send", variant="primary", scale=1)
            
            clear = gr.Button("Clear")
            
            gr.Examples(
                examples=[["I have digestive issues and anxiety"], ["What is Vata constitution?"], ["Foods for better sleep?"]],
                inputs=msg
            )
            
            msg.submit(self.chat, [msg, chatbot], [chatbot])
            submit.click(self.chat, [msg, chatbot], [chatbot])
            msg.submit(lambda: "", None, [msg])
            clear.click(lambda: None, None, [chatbot])
        
        return interface
    
    def launch(self, share: bool = None, server_port: int = None):
        if share is None:
            share = os.getenv("GRADIO_SHARE", "false").lower() == "true"
        if server_port is None:
            server_port = int(os.getenv("GRADIO_PORT", "7860"))
        
        interface = self.create_interface()
        interface.launch(share=share, server_port=server_port, server_name="127.0.0.1")

def main():
    app = AyurMindApp()
    app.launch()

if __name__ == "__main__":
    main()
