from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers.analyze import router as analyze_router
from services.text_detector import TextDetector
from services.image_detector import ImageDetector
from services.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    app.state.text_detector = TextDetector()
    app.state.image_detector = ImageDetector()
    yield
    # Shutdown (if needed)


app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

app.include_router(analyze_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)