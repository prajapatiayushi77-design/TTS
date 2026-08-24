# Professional Text-to-Speech Web Application

A modern, web-based text-to-speech application that converts unlimited-length text into high-quality audio with voice selection and download capabilities.

## Features

✨ **Core Features:**
- 📝 Convert unlimited text to speech (no character limits)
- 🎤 Male/Female voice selection
- 🎚️ Adjustable speaking rate (100-300 wpm)
- ⚡ Fast audio generation with checkpointing
- 💾 Download audio as WAV files
- 📱 Responsive, professional UI
- 🔄 Auto-cleanup of old files

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Web Application

```bash
python app.py
```

### 3. Open in Browser

Navigate to: **http://localhost:5000**

## Usage

### Web Interface

1. **Enter Text**: Paste or type your text in the text area
2. **Select Voice**: Choose between Male or Female voices
3. **Adjust Speed**: Use the slider to set speaking rate (100-300 words per minute)
4. **Generate**: Click "Generate Audio" button
5. **Download**: Listen in the player and download the WAV file

### Command Line (Original CLI)

For command-line usage, see the original main.py:

```bash
# Basic usage
python main.py --input yourfile.txt --output speech.wav

# With text input
python main.py --text "Hello, world!" --output hello.wav

# Custom settings
python main.py --input file.txt --output file.wav --rate 150 --chunk-size 400

# Resume interrupted job
python main.py --input file.txt --output file.wav --resume
```

## Project Structure

```
tts_project/
├── app.py                      # Flask web server
├── main.py                     # CLI entry point
├── text_chunker.py             # Text splitting logic
├── tts_engine.py               # TTS backend abstraction
├── audio_utils.py              # Audio merging
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── templates/
│   └── index.html              # Web interface
├── static/
│   ├── style.css               # Styling
│   └── script.js               # Frontend logic
├── downloads/                  # Generated audio files (auto-cleanup)
└── uploads/                    # Uploaded files (if needed)
```

## Technology Stack

- **Backend**: Flask (Python web framework)
- **TTS Engine**: pyttsx3 (offline, cross-platform)
- **Audio Processing**: pydub
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **UI Framework**: Custom modern design

## System Requirements

- **Python**: 3.8+
- **RAM**: 2GB minimum
- **Disk Space**: Depends on audio length (WAV format)
- **Network**: Not required (fully offline capable)

### Platform-Specific

**Windows:**
- Uses built-in SAPI5 for voice synthesis
- FFmpeg (optional, for MP3 export)

**macOS:**
- Uses built-in `say` command
- No additional installation needed

**Linux:**
- Requires: `sudo apt-get install espeak-ng ffmpeg`

## API Endpoints

### POST `/api/generate`
Generate audio from text.

**Request:**
```json
{
  "text": "Your text here",
  "gender": "female",  // or "male"
  "rate": 175          // 100-300 wpm
}
```

**Response:**
```json
{
  "job_id": "abc123",
  "status": "completed",
  "download_url": "/download/abc123_output.wav"
}
```

### GET `/download/<filename>`
Download generated audio file.

### GET `/api/voices`
Get available voices.

**Response:**
```json
{
  "male": [
    {"id": "voice_id", "name": "Voice Name"}
  ],
  "female": [
    {"id": "voice_id", "name": "Voice Name"}
  ]
}
```

### GET `/api/job/<job_id>`
Check job status.

## Configuration

Edit `app.py` to customize:

```python
# Maximum file size (default: 50MB)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

# Default speaking rate
rate = 175

# Default chunk size (characters)
chunk_size = 500

# Gap between chunks (milliseconds)
gap_ms = 150
```

## Troubleshooting

### Audio not generating?
- Check that pyttsx3 is installed: `pip install pyttsx3`
- On Linux, install espeak-ng: `sudo apt-get install espeak-ng`

### Voice selection not working?
- Voices may be platform-specific
- Male/Female categorization is automatic based on voice names
- Try a different operating system voice settings

### MP3 download not working?
- MP3 requires FFmpeg: install it first
- Use WAV format instead (no FFmpeg needed)

### Application won't start?
- Ensure Flask is installed: `pip install Flask`
- Check that port 5000 is available
- Try: `python app.py --host 0.0.0.0 --port 8000`

## Performance Tips

1. **Optimal Chunk Size**: 400-600 characters for best balance
2. **Speaking Rate**: 150-175 wpm sounds most natural
3. **Long Documents**: Application handles any length, may take time
4. **File Size**: WAV files are typically 50-100MB per hour of audio

## Future Enhancements

- [ ] MP3 export with FFmpeg auto-detection
- [ ] Upload text files
- [ ] Pause/Resume audio playback
- [ ] Multiple output formats
- [ ] User accounts and history
- [ ] Batch processing
- [ ] Custom voice profiles
- [ ] SSML support for advanced formatting

## License

This project is open source. Feel free to modify and use as needed.

## Support

For issues or questions, check the following:
- Ensure all dependencies are installed
- Verify your Python version is 3.8+
- Check that no other application is using port 5000
- Review the console output for error messages

## Credits

Built with:
- pyttsx3 for offline text-to-speech
- Flask for web framework
- Modern web design principles
