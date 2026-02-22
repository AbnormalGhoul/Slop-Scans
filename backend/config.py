import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    
    SIGHTENGINE_API_USER: str = os.getenv("SIGHTENGINE_API_USER")
    SIGHTENGINE_API_SECRET: str = os.getenv("SIGHTENGINE_API_SECRET")
    
    APP_NAME: str = os.getenv("APP_NAME", "Slop Scans")
    DEBUG: bool = os.getenv("DEBUG", "True") == "True"

    TEXT_MODEL_NAME: str = os.getenv("TEXT_MODEL_NAME", "desklib/ai-text-detector-v1.01")
    HF_TOKEN: str = os.getenv("HF_TOKEN")

    TEXT_AI_THRESHOLD: float = float(os.getenv("TEXT_AI_THRESHOLD", 0.5))
    IMAGE_AI_THRESHOLD: float = float(os.getenv("IMAGE_AI_THRESHOLD", 0.5))

    MAX_TEXT_LENGTH: int = int(os.getenv("MAX_TEXT_LENGTH", 768))

settings = Settings()