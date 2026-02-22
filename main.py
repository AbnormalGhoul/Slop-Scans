from fastapi import FastAPI
from routers.analyze import router as analyze_router
from services.text_detector import TextDetector
from services.image_detector import ImageDetector
from services.config import settings

app = FastAPI(title=settings.APP_NAME)

@app.on_event("startup")
async def startup_event():
    app.state.text_detector = TextDetector()
    app.state.image_detector = ImageDetector()

app.include_router(analyze_router, prefix="/api")