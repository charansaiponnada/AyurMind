"""
Gradio Chat Interface
"""

import os
import sys
from pathlib import Path
import gradio as gr
from dotenv import load_dotenv
import logging

# Setup logger with unique name to avoid conflicts
app_logger = logging.getLogger('ayurmind.ui')
app_logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(levelname)s:%(name)s:%(message)s'))
app_logger.addHandler(handler)

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.rag.embeddings import EmbeddingGenerator
from src.rag.vectorstore import AyurvedicVectorStore
from src.rag.retriever import RAGRetriever
from src.llm.google_client import GoogleClient
from src.llm.openai_client import OpenAIClient
from src.llm.local_client import OllamaClient # Import OllamaClient
from src.agents.prakriti_agent import PrakritiAgent
from src.agents.dosha_agent import DoshaAgent
from src.agents.treatment_agent import TreatmentAgent
from src.agents.orchestrator import OrchestratorAgent

load_dotenv()


class AyurMindApp:
    """AyurMind Gradio Application"""
    
    def __init__(self):
        """Initialize the application"""
        app_logger.info("Initializing AyurMind application...")
        
        # Initialize RAG components
        self.vectorstore = AyurvedicVectorStore()
        self.embedding_generator = EmbeddingGenerator()
        self.retriever = RAGRetriever(self.vectorstore, self.embedding_generator)
        
        # Initialize LLM client - with Local preference, then OpenAI, then Google fallback
        self.llm_client = None
        use_local_llm = os.getenv("USE_LOCAL_LLM", "false").lower() == "true"
        use_openai = os.getenv("USE_OPENAI", "false").lower() == "true"

        if use_local_llm:
            try:
                self.llm_client = OllamaClient()
                app_logger.info(f"✅ Using Local client with model: {self.llm_client.model_name}")
            except Exception as e:
                app_logger.warning(f"Local LLM Client failed to initialize: {e}. Falling back to other clients.")

        if self.llm_client is None and use_openai:
            try:
                self.llm_client = OpenAIClient()
                app_logger.info(f"✅ Using OpenAI client with model: {self.llm_client.model_name}")
            except Exception as e:
                app_logger.warning(f"OpenAI Client failed to initialize: {e}. Falling back to Google Client.")

        if self.llm_client is None: # If no other client was chosen or failed
            try:
                self.llm_client = GoogleClient()
                app_logger.info(f"✅ Using Google client with model: {self.llm_client.model_name}")
            except Exception as e:
                app_logger.error(f"Failed to initialize GoogleClient: {e}. No LLM client available.")
                raise e # Critical failure if no client can be initialized
        
        
        # Initialize agents
        self.prakriti_agent = PrakritiAgent(self.retriever, self.llm_client)
        self.dosha_agent = DoshaAgent(self.retriever, self.llm_client)
        self.treatment_agent = TreatmentAgent(self.retriever, self.llm_client)
        
        # Initialize orchestrator
        self.orchestrator = OrchestratorAgent(
            self.prakriti_agent,
            self.dosha_agent,
            self.treatment_agent,
            self.llm_client
        )
        
        app_logger.info("✓ AyurMind initialized successfully")
    
    # def chat(self, message: str, history: list):
    #     if not message.strip():
    #         return "Please enter a question."
        
    #     try:
    #         response = self.orchestrator.simple_query(message)
    #         return response
    #     except Exception as e:
    #         return f"Error: {str(e)}. Please try again."
        def chat(self, message: str, history: list, user_mode: str):
            history = history or []
    
            if not message.strip():
                return history
    
            try:
                # add user message
                history.append({"role": "user", "content": message})
    
                # Pass the user_mode to the orchestrator, converting to lower case
                response = self.orchestrator.simple_query(message, history, user_mode=user_mode.lower())
    
                # Extract the final_response text from the dictionary
                response_text = response.get('final_response', str(response))
    
                # add assistant message
                history.append({"role": "assistant", "content": response_text})
    
                return history
    
            except Exception as e:
                history.append({
                    "role": "assistant",
                    "content": f"Error: {str(e)}. Please try again."
                })
                return history
    
        
        def create_interface(self):
            with gr.Blocks(title="AyurMind") as interface:
                gr.HTML('<div style="text-align:center; padding:2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color:white; border-radius:10px;"><h1>🌿 AyurMind</h1><p style="font-size:1.2rem;">AI-Powered Ayurvedic Consultation</p></div>')
                
                gr.HTML('<div style="background:#fff3cd; border:1px solid #ffc107; padding:1rem; border-radius:5px; margin:1rem 0;"><strong>⚠️ Disclaimer:</strong> Educational only. Not medical advice. Consult professionals.</div>')
                
                with gr.Row():
                    with gr.Column(scale=4):
                        chatbot = gr.Chatbot(height=500, label="Consultation")
                    with gr.Column(scale=1):
                        user_mode = gr.Radio(
                            ["Beginner", "Intermediate", "Expert"],
                            label="Select Your Expertise Level",
                            value="Expert",
                            info="Choose the level of detail for your consultation."
                        )
                
                with gr.Row():
                    msg = gr.Textbox(label="Your Question", placeholder="Describe your concern...", scale=4)
                    submit = gr.Button("Send", variant="primary", scale=1)
                
                clear = gr.Button("Clear")
                
                gr.Examples(
                    examples=[["I have digestive issues and anxiety"], ["What is Vata constitution?"], ["Foods for better sleep?"]],
                    inputs=msg
                )
                
                # Update event handlers to include the user_mode input
                msg.submit(self.chat, [msg, chatbot, user_mode], [chatbot])
                submit.click(self.chat, [msg, chatbot, user_mode], [chatbot]).then(lambda: "", None, [msg])
                clear.click(lambda: None, None, [chatbot])
            
            return interface
        
        def launch(self, share: bool = None, server_port: int = None):
            if share is None:
                share = os.getenv("GRADIO_SHARE", "false").lower() == "true"
            if server_port is None:
                server_port = int(os.getenv("GRADIO_PORT", "7860"))
            
            # Use 0.0.0.0 when sharing so the public link works
            server_name = "0.0.0.0" if share else "127.0.0.1"
            
            interface = self.create_interface()
            interface.launch(share=share, server_port=server_port, server_name=server_name)

def main():
    app = AyurMindApp()
    app.launch()

if __name__ == "__main__":
    main()
