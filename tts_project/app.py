#!/usr/bin/env python3
"""
Flask web application for unlimited-length text-to-speech.
Provides a professional UI for generating audio with voice selection.
"""

import os
import uuid
import threading
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file, send_from_directory
from text_chunker import chunk_text
from tts_engine import get_backend
from audio_utils import concatenate_wavs
import shutil

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['DOWNLOADS_FOLDER'] = 'downloads'

# Create necessary folders
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['DOWNLOADS_FOLDER'], exist_ok=True)

# Store job status
jobs = {}


def get_available_voices():
    """Get available voices from pyttsx3"""
    try:
        from tts_engine import Pyttsx3Backend
        backend = Pyttsx3Backend()
        voices = backend.list_voices()
        
        # Categorize voices by gender (heuristic based on name)
        male_voices = []
        female_voices = []
        
        for voice_id, name, langs in voices:
            if any(term in name.lower() for term in ['man', 'male', 'david', 'mark', 'michael', 'george']):
                male_voices.append({'id': voice_id, 'name': name})
            elif any(term in name.lower() for term in ['woman', 'female', 'zira', 'victoria', 'susan', 'sarah']):
                female_voices.append({'id': voice_id, 'name': name})
            else:
                # Default to female if unclear
                female_voices.append({'id': voice_id, 'name': name})
        
        return {
            'male': male_voices if male_voices else [voices[0] if voices else None],
            'female': female_voices if female_voices else [voices[0] if voices else None]
        }
    except Exception as e:
        print(f"Error getting voices: {e}")
        return {'male': [], 'female': []}


def synthesize_audio(text, output_path, voice_id, rate=175):
    """Synthesize text to speech"""
    try:
        chunks = chunk_text(text, max_chars=500)
        if not chunks:
            raise ValueError("Text is empty")
        
        ckpt_dir = f".tts_checkpoints_{uuid.uuid4().hex}"
        os.makedirs(ckpt_dir, exist_ok=True)
        
        backend = get_backend("pyttsx3")
        chunk_paths = []
        
        for i, chunk in enumerate(chunks):
            chunk_path = os.path.join(ckpt_dir, f"chunk_{i:06d}.wav")
            chunk_paths.append(chunk_path)
            backend.synth(chunk, chunk_path, voice_id=voice_id, rate=rate)
        
        # Merge chunks
        concatenate_wavs(chunk_paths, output_path, gap_ms=150)
        
        # Cleanup
        shutil.rmtree(ckpt_dir)
        return True
    except Exception as e:
        print(f"Synthesis error: {e}")
        return False


@app.route('/')
def index():
    """Serve the main page"""
    voices = get_available_voices()
    return render_template('index.html', voices=voices)


@app.route('/api/generate', methods=['POST'])
def generate_audio():
    """Generate audio from text"""
    try:
        data = request.json
        text = data.get('text', '').strip()
        gender = data.get('gender', 'female')
        rate = int(data.get('rate', 175))
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        if len(text) > 50000:
            return jsonify({'error': 'Text exceeds 50,000 characters'}), 400
        
        # Get voice
        voices = get_available_voices()
        voice_list = voices.get(gender, [])
        if not voice_list:
            return jsonify({'error': f'No {gender} voices available'}), 400
        
        voice_id = voice_list[0]['id']
        
        # Generate unique filename
        job_id = str(uuid.uuid4())[:8]
        output_path = os.path.join(app.config['DOWNLOADS_FOLDER'], f'{job_id}_output.wav')
        
        # Synthesize (this blocks, but Flask can handle it)
        jobs[job_id] = {'status': 'generating', 'text': text[:100]}
        
        success = synthesize_audio(text, output_path, voice_id, rate)
        
        if success and os.path.exists(output_path):
            jobs[job_id]['status'] = 'completed'
            jobs[job_id]['filename'] = f'{job_id}_output.wav'
            return jsonify({
                'job_id': job_id,
                'status': 'completed',
                'download_url': f'/download/{job_id}_output.wav'
            })
        else:
            jobs[job_id]['status'] = 'failed'
            return jsonify({'error': 'Failed to generate audio'}), 500
    
    except Exception as e:
        print(f"API error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/download/<filename>')
def download_file(filename):
    """Download generated audio file"""
    try:
        file_path = os.path.join(app.config['DOWNLOADS_FOLDER'], filename)
        if os.path.exists(file_path):
            return send_file(
                file_path,
                as_attachment=True,
                download_name=filename,
                mimetype='audio/wav'
            )
        return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        print(f"Download error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/voices', methods=['GET'])
def get_voices():
    """Get available voices"""
    voices = get_available_voices()
    return jsonify(voices)


@app.route('/api/job/<job_id>', methods=['GET'])
def get_job_status(job_id):
    """Get job status"""
    job = jobs.get(job_id)
    if job:
        return jsonify(job)
    return jsonify({'error': 'Job not found'}), 404


# Cleanup old files periodically
def cleanup_old_files():
    """Remove files older than 1 hour"""
    import time
    while True:
        try:
            now = time.time()
            for filename in os.listdir(app.config['DOWNLOADS_FOLDER']):
                filepath = os.path.join(app.config['DOWNLOADS_FOLDER'], filename)
                if os.path.isfile(filepath) and now - os.path.getmtime(filepath) > 3600:
                    os.remove(filepath)
        except Exception as e:
            print(f"Cleanup error: {e}")
        time.sleep(300)  # Check every 5 minutes


if __name__ == '__main__':
    # Start cleanup thread
    cleanup_thread = threading.Thread(target=cleanup_old_files, daemon=True)
    cleanup_thread.start()
    
    print("Starting TTS Web Application...")
    print("Open your browser to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
