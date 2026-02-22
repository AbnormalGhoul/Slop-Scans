from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from PIL import Image
import io

from services.text_detector import text_detector
from services.image_detector import image_detector
from config import settings

app = FastAPI(title=settings.APP_NAME)


class TextRequest(BaseModel):
    text: str


@app.get("/")
def root():
    return {"status": "Slop Scans backend running"}


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
    image = Image.open(io.BytesIO(contents)).convert("RGB")

    result = image_detector.predict(image)

    return {
        "type": "image",
        **result
    }