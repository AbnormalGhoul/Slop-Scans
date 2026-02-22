from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from PIL import Image
from pathlib import Path
import io
import glob
import os
from typing import Optional


import uvicorn

from services.text_detector import text_detector
from services.image_detector import image_detector
from config import settings

from detector_handler import run_detector

app = FastAPI(title=settings.APP_NAME, debug=True)

class TextRequest(BaseModel):
    text: str

class PageRequest(BaseModel):
    url: str

class DetectionResult(BaseModel):
    percentage: float
    ai_phrases: Optional[str] = None

@app.get("/")
def root():
    return {"status": "Slop Scans backend running"}

@app.post("/detect/page", response_model=DetectionResult)
def detect_page(request: PageRequest):
    result = run_detector(request.url)
    return result

@app.post("/detect/text")
def detect_text(request: TextRequest):
    result = text_detector.predict(request.text)
    return {
        "type": "text",
        **result
    }

@app.post("/detect/image")
async def detect_image(file: UploadFile = File(...)):
    contents = await file.read()
    result = image_detector.predict_from_bytes(contents)

    return {
        "type": "image",
        **result
    }

def delete_image(file_name):
    try:
        os.remove(file_name)
        print(f"Image {file_name} deleted successfully")
    except OSError as e:
        print(f"Error deleting image {file_name}: {e}")
        
def remove_double_quotes_from_file(input_file: str, output_file: str = None) -> str:
    """Remove double quotes and line breaks from a file and save to output file."""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Remove double quotes
        cleaned_content = content.replace('"', '')

        # Remove all line breaks (Windows + Unix safe)
        cleaned_content = cleaned_content.replace('\r', ' ').replace('\n', ' ')

        # Collapse multiple spaces into single space
        cleaned_content = re.sub(r'\s+', ' ', cleaned_content).strip()

        if output_file is None:
            if input_file.endswith('.txt'):
                output_file = input_file.replace('.txt', '_cleaned.txt')
            else:
                output_file = input_file + '_cleaned'

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)

        return f"Successfully cleaned file. Output saved to: {output_file}"

    except FileNotFoundError:
        return f"Error: File '{input_file}' not found"
    except Exception as e:
        return f"Error: {e}"
    
if __name__ == "__main__":

    print("\nRunning local detection tests...\n")

    # Text Test
    text_path = "data/transcription.txt"
    
    remove_double_quotes_from_file(text_path)  # Clean up text file before test

    if os.path.exists(text_path):
        with open(text_path, "r", encoding="utf-8") as f:
            text_content = f.read()

        text_result = text_detector.predict(text_content)

        print("TEXT RESULT:")
        print(text_result)
        print()
    else:
        print(f"Text file not found at {text_path}")

    # Image Test
    image_extensions = ["png", "jpg", "jpeg", "webp"]
    image_files = []

    for ext in image_extensions:
        image_files.extend(glob.glob(f"data/*.{ext}"))

    if image_files:
        image_path = image_files[0]  # take first match
        print(f"Using image: {image_path}")

        with open(image_path, "rb") as f:
            image_bytes = f.read()

        image_result = image_detector.predict_from_bytes(image_bytes)

        print("IMAGE RESULT:")
        print(image_result)
        print()
        
        delete_image(image_path)  # Clean up after test

    uvicorn.run(app, host="0.0.0.0", port=8000)
        
else:
    print("No supported image file found in /data/")