# AyurMind Deployment Guide

## 🚀 Deploy to Hugging Face Spaces (Recommended)

### Prerequisites
1. Create account at [huggingface.co](https://huggingface.co)
2. Have your API keys ready (Google Gemini or OpenAI)

### Steps

#### 1. Create New Space
- Go to https://huggingface.co/spaces
- Click **"Create new Space"**
- Name: `ayurmind`
- License: MIT
- SDK: **Gradio**
- Python version: 3.10
- Click **Create Space**

#### 2. Upload Files
You can use Git or the web interface:

**Option A: Using Git**
```bash
# Clone your HF Space repo
git clone https://huggingface.co/spaces/YOUR_USERNAME/ayurmind
cd ayurmind

# Copy your project files
cp -r /path/to/ayurmind_project/* .

# Commit and push
git add .
git commit -m "Initial deployment"
git push
```

**Option B: Using Web Interface**
- Upload these files via the web UI:
  - `app.py` (entry point)
  - `requirements.txt`
  - `src/` folder (entire directory)
  - `data/vectordb/` folder (if pre-built)
  - `scripts/02_build_vectordb.py` (to rebuild on startup if needed)

#### 3. Configure Secrets
In your Space settings:
- Go to **Settings** → **Repository secrets**
- Add your API keys:
  ```
  GOOGLE_API_KEY=your_key_here
  USE_OPENAI=false
  ```
  or
  ```
  OPENAI_API_KEY=your_key_here
  USE_OPENAI=true
  ```

#### 4. Handle Vector Database

**Option A: Pre-build locally and upload**
```bash
# Build locally
python scripts/02_build_vectordb.py

# Upload data/vectordb/ folder to HF Space
```

**Option B: Build on first startup**
Add to `app.py` before launching:
```python
import os
if not os.path.exists("data/vectordb/chroma.sqlite3"):
    print("Building vector database...")
    os.system("python scripts/02_build_vectordb.py")
```

#### 5. Deploy
- HF Spaces automatically builds and deploys
- Your app will be live at: `https://huggingface.co/spaces/YOUR_USERNAME/ayurmind`
- Share this URL with anyone!

---

## 🐳 Alternative: Docker Deployment

See `Dockerfile` for containerized deployment to any platform:
- AWS ECS/EKS
- Azure Container Apps
- Google Cloud Run
- DigitalOcean
- Self-hosted servers

```bash
# Build
docker build -t ayurmind .

# Run
docker run -p 7860:7860 -e GOOGLE_API_KEY=your_key ayurmind
```

---

## 🔧 Alternative: ngrok (Quick Local Sharing)

If Gradio share doesn't work:

```bash
# Terminal 1: Run app locally
python scripts/04_run_app.py

# Terminal 2: Create tunnel
ngrok http 7860
```

Share the ngrok URL (e.g., `https://abc123.ngrok.io`)

---

## 📝 Notes

### Data Requirements
- Vector database (~100MB+) needs to be included or built on startup
- Pre-building locally and uploading is faster for first load

### API Keys
- Never commit API keys to git
- Use environment variables or secrets management
- HF Spaces provides secure secrets storage

### Resource Limits
- HF Spaces free tier: 2 vCPU, 16GB RAM, 50GB storage
- Upgrade to paid tier for better performance
- Consider caching for embedded models

### Monitoring
- HF Spaces shows logs and usage metrics
- Set up error tracking if needed
- Monitor API usage costs

---

## 🆘 Troubleshooting

**Issue: Share link doesn't work**
- Use ngrok instead
- Deploy to HF Spaces for permanent hosting

**Issue: Vector database missing**
- Run `python scripts/02_build_vectordb.py` first
- Or include build step in deployment

**Issue: Out of memory**
- Upgrade HF Space tier
- Use smaller embedding model
- Optimize vector database size

**Issue: Slow loading**
- Pre-build vector database
- Cache sentence-transformers model
- Use faster embedding model
