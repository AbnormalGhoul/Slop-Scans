#!/usr/bin/env bash

set -e

# Create venv
python3.10 -m venv venv
source venv/bin/activate

# Rquirements installation
pip install --upgrade pip
pip install -r requirements.txt
python -c "import nltk; nltk.download('punkt')"

echo "Setup complete. Activate venv with: source venv/bin/activate"
