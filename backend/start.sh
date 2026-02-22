#!/usr/bin/env bash

set -e

source .venv/bin/activate

# export APP_ENV=development

uvicorn main:app --host 0.0.0.0 --port 8000 --reload