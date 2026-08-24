# 🚀 TTS Deployment Quick Reference

## Local Development

```bash
# Run Flask web server
python app.py

# Access at: http://localhost:5000
```

---

## Deploy to Vercel (Global, Recommended)

### One-Time Setup
```bash
# Install Vercel CLI
npm install -g vercel

# Push to GitHub first
git init
git add .
git commit -m "TTS application"
git remote add origin https://github.com/YOUR_USERNAME/tts-project
git push -u origin main
```

### Deploy
```bash
# In project directory
vercel

# Follow prompts, your app will be live!
```

**Your URL:** `https://your-project.vercel.app`

---

## Deploy to Railway (Python-Friendly)

### Steps
1. Go to https://railway.app
2. Click "New Project" → "Deploy from GitHub"
3. Select your repository
4. Railway auto-detects Dockerfile
5. Click "Deploy"

**Your URL:** `https://your-app.railway.app`

---

## Deploy to Render (Easiest)

### Steps
1. Go to https://render.com
2. New → Web Service
3. Connect GitHub
4. Select repository
5. Set start command: `gunicorn --bind 0.0.0.0:$PORT app:app`
6. Click "Create Web Service"

**Your URL:** `https://your-app.onrender.com`

---

## Use CLI Tool

```bash
# Text to audio
python main.py --text "Hello world" --output hello.wav

# File to audio
python main.py --input book.txt --output book.wav

# Custom settings
python main.py --input file.txt --output file.wav --rate 150

# Resume interrupted job
python main.py --input file.txt --output file.wav --resume
```

---

## Install Dependencies

```bash
# Basic (local web server)
pip install -r requirements.txt

# Production (all TTS backends)
pip install -r requirements-prod.txt

# Manual
pip install Flask edge-tts pyttsx3 pydub tqdm
```

---

## API Endpoints

### Local Server (http://localhost:5000)

**Generate Audio**
```bash
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello world",
    "gender": "female",
    "rate": 175
  }'
```

**Get Voices**
```bash
curl http://localhost:5000/api/voices
```

### Deployed Server
Replace `localhost:5000` with your deployment URL

---

## Environment Variables

Create `.env.local`:
```env
PYTHON_VERSION=3.11
DEBUG=False
TTS_BACKEND=edge
MAX_TEXT_LENGTH=50000
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 5000 in use | `python app.py --port 8000` |
| Audio not generating | Install edge-tts: `pip install edge-tts` |
| Deployment failed | Check GitHub push, verify requirements.txt |
| API timeout | Use Railway (higher limits than Vercel) |
| Voices not available | Check Vercel logs, ensure edge-tts installed |

---

## Performance Tips

- **Optimal text length:** 100-10,000 words
- **Optimal rate:** 150-175 wpm
- **Optimal chunk size:** 400-600 characters
- **Expected time:** 1-5 seconds per 1,000 words

---

## File Locations

| File | Purpose |
|------|---------|
| `app.py` | Flask web server |
| `main.py` | CLI tool |
| `vercel.json` | Vercel config |
| `Dockerfile` | Container for Railway |
| `requirements.txt` | Core dependencies |
| `api/generate.py` | Vercel API endpoint |
| `static/` | Frontend assets |
| `templates/` | HTML templates |

---

## Useful Links

- Vercel: https://vercel.com
- Railway: https://railway.app
- Render: https://render.com
- GitHub: https://github.com
- npm: https://nodejs.org

---

## Interactive Setup

```bash
python setup.py
```

Guided wizard for setup and deployment.

---

**Quick Command Summary:**

```bash
# Local
python app.py

# Deploy to Vercel
npm install -g vercel && vercel

# Deploy to Railway
# (via web dashboard)

# CLI usage
python main.py --text "text" --output audio.wav
```

---

Made for quick reference during deployment! 🚀
