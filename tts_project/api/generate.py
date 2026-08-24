import json
import os
import sys
from pathlib import Path
import shutil
import tempfile
import base64

# Add parent directory to path
sys.path.insert(0, '/var/task')

def handler(request):
    """
    Vercel serverless function handler for text-to-speech generation.
    """
    
    # Enable CORS
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
    }
    
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': 'OK'
        }
    
    if request.method != 'POST':
        return {
            'statusCode': 405,
            'headers': headers,
            'body': json.dumps({'error': 'Method not allowed'})
        }
    
    try:
        body = json.loads(request.body) if isinstance(request.body, str) else request.body
    except:
        return {
            'statusCode': 400,
            'headers': headers,
            'body': json.dumps({'error': 'Invalid JSON'})
        }
    
    text = body.get('text', '').strip()
    gender = body.get('gender', 'female')
    rate = body.get('rate', 175)
    backend_name = body.get('backend', 'edge')  # Default to edge-tts for cloud
    
    if not text:
        return {
            'statusCode': 400,
            'headers': headers,
            'body': json.dumps({'error': 'Text is required'})
        }
    
    if len(text) > 50000:
        return {
            'statusCode': 400,
            'headers': headers,
            'body': json.dumps({'error': 'Text exceeds 50,000 characters'})
        }
    
    try:
        # Use temporary directory for audio generation
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, 'output.wav')
            
            # Synthesize audio
            success = synthesize_audio_serverless(
                text, 
                output_path, 
                gender, 
                rate, 
                backend_name
            )
            
            if not success:
                return {
                    'statusCode': 500,
                    'headers': headers,
                    'body': json.dumps({'error': 'Failed to generate audio'})
                }
            
            # Read audio file and encode as base64
            with open(output_path, 'rb') as f:
                audio_data = base64.b64encode(f.read()).decode('utf-8')
            
            return {
                'statusCode': 200,
                'headers': {**headers, 'Content-Type': 'application/json'},
                'body': json.dumps({
                    'status': 'completed',
                    'audio': f'data:audio/wav;base64,{audio_data}',
                    'size': len(audio_data)
                })
            }
    
    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }


def synthesize_audio_serverless(text, output_path, gender, rate, backend_name):
    """Synthesize text to speech for serverless environment"""
    try:
        # For serverless, we use edge-tts (cloud-based)
        if backend_name == 'edge':
            return synthesize_with_edge_tts(text, output_path, gender)
        else:
            # Fallback to pyttsx3 if edge-tts not available
            return synthesize_with_pyttsx3(text, output_path, gender, rate)
    except Exception as e:
        print(f"Synthesis error: {e}")
        return False


def synthesize_with_edge_tts(text, output_path, gender):
    """Use edge-tts for cloud-based synthesis (serverless-friendly)"""
    try:
        import edge_tts
        import asyncio
        
        # Map gender to voice
        voice_map = {
            'male': 'en-US-GuyNeural',
            'female': 'en-US-AriaNeural'
        }
        voice_id = voice_map.get(gender, 'en-US-AriaNeural')
        
        async def generate():
            communicate = edge_tts.Communicate(text, voice=voice_id)
            mp3_path = output_path.replace('.wav', '.mp3')
            await communicate.save(mp3_path)
            
            # Convert MP3 to WAV
            from pydub import AudioSegment
            audio = AudioSegment.from_mp3(mp3_path)
            audio.export(output_path, format='wav')
            os.remove(mp3_path)
        
        asyncio.run(generate())
        return True
    except Exception as e:
        print(f"Edge TTS error: {e}")
        return False


def synthesize_with_pyttsx3(text, output_path, gender, rate):
    """Fallback to pyttsx3"""
    try:
        from tts_engine import Pyttsx3Backend
        backend = Pyttsx3Backend()
        
        # Get voices and filter by gender
        voices = backend.list_voices()
        voice_id = None
        
        for vid, name, langs in voices:
            if gender == 'male' and any(term in name.lower() for term in ['man', 'male', 'david']):
                voice_id = vid
                break
            elif gender == 'female' and any(term in name.lower() for term in ['woman', 'female', 'zira']):
                voice_id = vid
                break
        
        if not voice_id and voices:
            voice_id = voices[0][0]
        
        backend.synth(text, output_path, voice_id=voice_id, rate=rate)
        return True
    except Exception as e:
        print(f"Pyttsx3 error: {e}")
        return False
