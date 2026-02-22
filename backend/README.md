# SLOP SCAN

## Setup (./setup.sh)
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python -c "import nltk; nltk.download('punkt')"

source venv/bin/activate
```

## .env file
Create a `.env` file in the project root:
```env
APP_NAME=AI Content Detection API
APP_ENV=development
DEBUG=True

TEXT_MODEL_NAME=SzegedAI/AI_Detector
IMAGE_MODEL_NAME=facebook/dino-vits16

TEXT_AI_THRESHOLD=0.5
IMAGE_AI_THRESHOLD=0.5

MAX_TEXT_LENGTH=512
```

## Run the Server (./start.sh)
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
Server should start at:
```
http://localhost:8000
http://localhost:8000/docs
```

## Notes
- Models will download automatically on first run.
- First startup may take time due to model loading.
- For GPU support, install the CUDA-enabled version of PyTorch.
- For best performance in WSL, keep the project inside the Linux filesystem (not `/mnt/c`).