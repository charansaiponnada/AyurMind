#!/usr/bin/env python3
"""
AyurMind - Hugging Face Spaces Entry Point
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from ui.gradio_app import AyurMindApp

if __name__ == "__main__":
    print("Launching AyurMind on Hugging Face Spaces...")
    app = AyurMindApp()
    # HF Spaces requires server_name="0.0.0.0" and will handle the public URL
    app.launch(share=False, server_port=7860)
