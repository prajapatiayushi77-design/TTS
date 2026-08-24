# Dockerfile for Railway, Render, and other container platforms
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=5000 \
    PYTHONPATH=/app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements-prod.txt .

# Install Python dependencies
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements-prod.txt

# Copy entire application
COPY . .

# Create necessary directories
RUN mkdir -p downloads uploads logs && \
    chmod -R 755 /app

# Expose port
EXPOSE 5000

# Run with Gunicorn
CMD exec gunicorn --bind 0.0.0.0:5000 --timeout 300 --workers 1 --worker-class sync --access-logfile - --error-logfile - wsgi:app

