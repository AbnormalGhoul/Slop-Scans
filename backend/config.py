import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "Slop Scans")
    DEBUG: bool = os.getenv("DEBUG", "True") == "True"

    TEXT_MODEL_NAME: str = os.getenv(
        "TEXT_MODEL_NAME",
        "desklib/ai-text-detector-v1.01"
    )

    IMAGE_MODEL_NAME: str = os.getenv(
        "IMAGE_MODEL_NAME",
        "facebook/dino-vits16"
    )

    TEXT_AI_THRESHOLD: float = float(os.getenv("TEXT_AI_THRESHOLD", 0.5))
    IMAGE_AI_THRESHOLD: float = float(os.getenv("IMAGE_AI_THRESHOLD", 0.5))

    MAX_TEXT_LENGTH: int = int(os.getenv("MAX_TEXT_LENGTH", 512))

settings = Settings()