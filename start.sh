#!/usr/bin/env bash

set -e

# Activate virtual environment
source venv/bin/activate

# Export environment variables (optional if using python-dotenv)
export APP_ENV=development

# Start FastAPI with auto-reload
uvicorn main:app --host 0.0.0.0 --port 8000 --reload