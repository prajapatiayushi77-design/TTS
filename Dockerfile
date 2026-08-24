FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app \
    PORT=5000

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY tts_project/requirements-prod.txt .
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements-prod.txt

COPY tts_project/ .
RUN mkdir -p downloads uploads logs && chmod -R 755 /app

EXPOSE 5000

CMD exec gunicorn --bind 0.0.0.0:${PORT:-5000} --timeout 300 --workers 1 --worker-class sync --access-logfile - --error-logfile - wsgi:app
