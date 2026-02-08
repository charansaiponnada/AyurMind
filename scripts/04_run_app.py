#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from ui.gradio_app import AyurMindApp

print("Launching AyurMind...")
print("To create a public share link, set GRADIO_SHARE=true in your .env file")
print("or run: python scripts/04_run_app.py --share")
print("-" * 50)

# Check for --share flag
share = "--share" in sys.argv

app = AyurMindApp()
app.launch(share=share)
