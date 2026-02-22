#!/usr/bin/env bash

set -e
sudo apt update
sudo apt install -y python3 python3-venv python3-dev build-essential
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python -c "import nltk; nltk.download('punkt')"