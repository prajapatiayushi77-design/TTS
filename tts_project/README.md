# Unlimited-Length Text-to-Speech

Convert text of **any length** — a tweet, an article, or a full book —
into a single continuous audio file. There's no per-request character
limit because the text is automatically split into small chunks,
synthesized individually, and stitched back together into one output
track. Total duration is bounded only by your disk space, not by any
engine or API limit.

## 🌐 Live Demo & Deployment

You can deploy this project to multiple platforms:
- **⚡ Vercel** (Serverless, global edge network) - Recommended
- **🚂 Railway** (Python-friendly, persistent storage)
- **🎨 Render** (Easy deployment, free tier)
- **🏠 Local Flask Server** (For development)

[See DEPLOYMENT_GUIDE.md for detailed deployment instructions](DEPLOYMENT_GUIDE.md)

## How it works

```
long text  ->  text_chunker.py  ->  many small chunks (sentence-safe)
                                          |
                                          v
                                 tts_engine.py (per chunk)
                                          |
                                          v
                          checkpoint/*.wav  (one file per chunk)
                                          |
                                          v
                            audio_utils.py -> final merged file
```

- **Chunking** never cuts a sentence in half; it packs sentences into
  chunks up to a configurable character limit, breaking at paragraph
  boundaries when convenient.
- **Checkpointing**: every chunk's audio is saved to disk with a
  sequence number before merging. If the process crashes, is
  rate-limited, or you Ctrl-C it halfway through a 3-hour audiobook,
  re-run with `--resume` and it picks up exactly where it left off
  instead of starting over.
- **Backends are pluggable** (see `tts_engine.py`) — swap engines
  without touching the chunking or merging logic.

## 🚀 Quick Start

### Web Interface (Recommended)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the web server
python app.py

# 3. Open your browser
# Visit: http://localhost:5000
```

Features:
- 🎤 Male/Female voice selection
- 🎚️ Adjustable speaking rate (100-300 wpm)
- 📝 Unlimited text length
- ⚡ Fast audio generation
- 💾 One-click download

### Command Line

```bash
# Convert a text file
python main.py --input book.txt --output book.wav

# Convert typed text
python main.py --text "Hello, world!" --output hello.wav

# Custom settings
python main.py --input file.txt --output file.wav --rate 150 --chunk-size 400

# Resume interrupted job
python main.py --input file.txt --output file.wav --resume
```

## Setup

### Windows
```bash
pip install -r requirements.txt
python app.py
```

### macOS (uses built-in `say` voices)
```bash
pip install -r requirements.txt
python app.py
```

### Linux
```bash
# Install system dependencies
sudo apt-get install espeak-ng ffmpeg

# Install Python dependencies
pip install -r requirements.txt
python app.py
```

## Features

✨ **Core Features:**
- 📝 Convert unlimited-length text to speech
- 🎤 Multiple voice selection (Male, Female)
- 🎚️ Adjustable speaking rate
- ⚡ Fast processing with checkpointing
- 💾 Download as WAV (no FFmpeg needed)
- 🔄 Resume interrupted jobs
- 📱 Mobile-friendly web interface
- 🌍 Deploy to any cloud platform

## Project Structure

```
tts_project/
├── app.py                      # Flask web application
├── main.py                     # CLI entry point
├── text_chunker.py             # Text splitting logic
├── tts_engine.py               # TTS backend abstraction
├── audio_utils.py              # Audio merging
├── setup.py                    # Setup & deployment helper
├── api/                        # Vercel serverless functions
│   ├── generate.py            # Audio generation endpoint
│   └── voices.py              # Voice list endpoint
├── templates/
│   └── index.html             # Web UI
├── static/
│   ├── style.css              # Styling
│   └── script.js              # Frontend logic
├── vercel.json                # Vercel configuration
├── Dockerfile                 # Container for Railway/Render
├── requirements.txt           # Core dependencies
├── requirements-prod.txt      # Production dependencies
└── DEPLOYMENT_GUIDE.md        # Detailed deployment guide
```

## Usage

### Web Interface

1. **Enter your text** in the text area (or paste a long document)
2. **Choose voice gender** (Male or Female)
3. **Adjust speaking rate** (100-300 words per minute)
4. **Click "Generate Audio"**
5. **Listen and download**

### API Endpoints (Web Server)

```
POST /api/generate
{
  "text": "Your text here",
  "gender": "female",
  "rate": 175
}

GET /api/voices
Returns available voices
```

## Deployment Options

### 🌟 Vercel (Recommended - Fastest Setup)

```bash
# 1. Push to GitHub
git push origin main

# 2. Install Vercel CLI
npm install -g vercel

# 3. Deploy
vercel
```

Your app will be live at: `https://your-app.vercel.app`

### 🚂 Railway

```bash
# 1. Push to GitHub
# 2. Go to https://railway.app
# 3. Create new project from GitHub repo
# 4. Railway auto-deploys using Dockerfile
```

### 🎨 Render

```bash
# 1. Push to GitHub
# 2. Go to https://render.com
# 3. Create new web service from GitHub
# 4. Render auto-deploys using render.yaml
```

### 🏠 Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run Flask server
python app.py

# Open browser
# http://localhost:5000
```

[Full deployment guide →](DEPLOYMENT_GUIDE.md)

## Configuration

Edit `app.py` to customize:

```python
# Maximum file size (default: 50MB)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

# Default speaking rate
rate = 175

# Default chunk size
chunk_size = 500

# Gap between chunks (ms)
gap_ms = 150
```

## Troubleshooting

### "Audio not generating?"
- Check dependencies: `pip install -r requirements.txt`
- Linux: `sudo apt-get install espeak-ng ffmpeg`

### "Port already in use?"
- Change port in `app.py`: `app.run(port=8000)`

### "Module not found?"
- Install all dependencies: `pip install -r requirements-prod.txt`

### "Slow generation?"
- Shorter texts = faster processing
- Optimal chunk size: 400-600 characters

## Performance Tips

- **Optimal rate**: 150-175 wpm sounds most natural
- **Optimal chunk size**: 400-600 characters
- **Long documents**: App handles any length, respects your time
- **File size**: ~50-100MB per hour of audio

## Keyboard Shortcuts

- `Ctrl+Enter`: Generate audio (web interface)

## System Requirements

- **Python**: 3.8+
- **RAM**: 2GB minimum
- **Disk**: Depends on audio length
- **Network**: Not required (works offline locally)

## License

Open source - feel free to modify and use as needed.

## Support

- **Issues?** Check DEPLOYMENT_GUIDE.md
- **Stuck?** Run `python setup.py` for guided setup
- **Need help?** Check the troubleshooting section above

---

**Made with ❤️ for unlimited audio generation**


```bash
# From a text file, any length
python3 main.py --input book.txt --output book.mp3

# From literal text
python3 main.py --text "Hello there, this can be as long as you like." --output hello.wav

# Resume an interrupted long job
python3 main.py --input book.txt --output book.mp3 --resume
```

## Options

| Flag           | Default   | Description                                                       |
|----------------|-----------|---------------------------------------------------------------------|
| `--input`      | —         | Path to a `.txt` file (mutually exclusive with `--text`)            |
| `--text`       | —         | Literal text on the command line                                    |
| `--output`     | required  | Output path, e.g. `out.mp3` / `out.wav`                             |
| `--backend`    | `pyttsx3` | `pyttsx3` (offline), `edge` (online, neural), `gtts` (online)        |
| `--chunk-size` | `500`     | Max characters per internal chunk                                    |
| `--gap-ms`     | `150`     | Silence inserted between chunks, in milliseconds                     |
| `--rate`       | `175`     | Speaking rate (pyttsx3)                                              |
| `--voice-id`   | —         | Backend-specific voice ID                                            |
| `--list-voices`| —         | List available pyttsx3 voices and exit                               |
| `--resume`     | off       | Continue a previously interrupted run for the same `--output`        |

## Choosing a backend

- **`pyttsx3` (default)** — fully offline, no internet or API key
  required, zero per-call limits. Voice quality is robotic but this is
  the most reliable option for very long or unattended jobs (e.g. on a
  server with no outbound internet).
- **`edge`** — Microsoft Edge's free neural voices. Much more natural
  sounding. Requires internet at synth time and the `edge-tts` package
  (`pip install edge-tts`). List voices with:
  `python3 -c "import asyncio, edge_tts; print(asyncio.run(edge_tts.list_voices()))"`
- **`gtts`** — Google Translate's TTS. Requires internet and
  `pip install gTTS`.

Both online backends are still processed through the same chunking and
checkpointing pipeline, so "unlimited length" applies to them too —
the only difference is where the actual audio rendering happens.

## Extending it

To add a new engine (e.g. a paid cloud API or a local neural TTS model
like Coqui/XTTS or Bark for higher quality output):

1. Add a class to `tts_engine.py` implementing `synth(text, out_wav_path, **opts)`.
2. Register it in the `_BACKENDS` dict at the bottom of that file.
3. Use it with `--backend your_new_name`.

Everything else (chunking, checkpointing, merging, resuming) works
unchanged for any backend you add.

## Tested

This project was verified end-to-end on a ~30,000-character input
(split into 120 chunks), producing a single continuous ~27-minute audio
file with correct sentence boundaries, and confirmed to correctly
resume after being interrupted partway through a run.
