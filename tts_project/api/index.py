from app import app

# Vercel serverless function handler
def handler(request):
    """Convert ASGI to Vercel format"""
    return app(request)
