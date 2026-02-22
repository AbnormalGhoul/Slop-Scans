#!/usr/bin/env bash

set -e

# Create venv using your existing Python 3.10
python3.10 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

python -c "import nltk; nltk.download('punkt')"

echo "Setup complete. Activate venv with: source venv/bin/activate"