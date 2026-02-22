from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import List

router = APIRouter()

class AnalyzeRequest(BaseModel):
    text: str
    images: List[str]  # List of image URLs or base64 strings


@router.post("/analyze")
async def analyze_content(request: Request, payload: AnalyzeRequest):

    text_detector = request.app.state.text_detector
    image_detector = request.app.state.image_detector

    text_result = text_detector.analyze(payload.text)
    image_result = image_detector.analyze(payload.images)

    return {
        "text_analysis": text_result,
        "image_analysis": image_result
    }