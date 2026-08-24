import json

def handler(request):
    """Get available voices"""
    
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
    }
    
    if request.method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': 'OK'
        }
    
    voices = {
        'male': [
            {'id': 'en-US-GuyNeural', 'name': 'Guy (Microsoft)'},
            {'id': 'en-US-JacobNeural', 'name': 'Jacob (Microsoft)'}
        ],
        'female': [
            {'id': 'en-US-AriaNeural', 'name': 'Aria (Microsoft)'},
            {'id': 'en-US-AvaNeural', 'name': 'Ava (Microsoft)'},
            {'id': 'en-US-JennyNeural', 'name': 'Jenny (Microsoft)'},
        ]
    }
    
    return {
        'statusCode': 200,
        'headers': headers,
        'body': json.dumps(voices)
    }
