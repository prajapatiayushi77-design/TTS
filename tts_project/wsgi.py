#!/usr/bin/env python3
"""
WSGI entry point for production deployment
Works with Gunicorn, Railway, and other production servers
"""

from app import app

if __name__ == "__main__":
    app.run()
