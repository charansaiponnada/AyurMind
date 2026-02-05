# AyurMind - Complete Installation Guide

## Quick Start (5 Minutes)

### 1. System Requirements
- Python 3.9 or higher
- 8GB RAM minimum (16GB recommended)
- 5GB free disk space
- Internet connection (for API or scraping)

### 2. Installation Steps

```bash
# Clone or extract the project
cd ayurmind_final

# Create virtual environment
python -m venv venv

# Activate (choose your OS)
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env  # or use any text editor

# Add your OpenRouter API key (FREE - get at https://openrouter.ai/keys)
OPENROUTER_API_KEY=sk-or-v1-your-key-here
```

### 3. Run the Pipeline

```bash
# Step 1: Scrape Ayurvedic texts (15-30 minutes)
python scripts/01_scrape_data.py

# Step 2: Build vector database (5-10 minutes)
python scripts/02_build_vectordb.py

# Step 3: Test RAG retrieval (1 minute)
python scripts/03_test_rag.py

# Step 4: Launch the app! 🚀
python scripts/04_run_app.py
```

Open http://localhost:7860 in your browser!

## Detailed Instructions

See README.md for full documentation.

## Troubleshooting

**Problem**: ModuleNotFoundError
**Solution**: Make sure you activated venv and ran `pip install -r requirements.txt`

**Problem**: No API key error
**Solution**: Get free key at https://openrouter.ai/keys and add to .env

**Problem**: Scraper fails
**Solution**: Check internet connection, increase REQUEST_DELAY in .env

## Next Steps

1. Try example queries in the chat interface
2. Experiment with different questions
3. Read the research paper (docs/research_proposal.docx)
4. Explore the code in src/

Enjoy! 🌿
