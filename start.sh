#!/bin/sh
set -eu

exec gunicorn --bind "0.0.0.0:${PORT:-5000}" --timeout 300 --workers 1 --worker-class sync --access-logfile - --error-logfile - wsgi:app
