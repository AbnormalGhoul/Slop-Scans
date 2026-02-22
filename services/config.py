import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """
    Centralized configuration class.
    Loads values from .env and provides defaults.
    """

    APP_NAME: str = os.getenv("APP_NAME", "AI Detector")
    DEBUG: bool = os.getenv("DEBUG", "False") == "True"

    TEXT_MODEL_NAME: str = os.getenv("TEXT_MODEL_NAME")
    IMAGE_MODEL_NAME: str = os.getenv("IMAGE_MODEL_NAME")

    TEXT_AI_THRESHOLD: float = float(os.getenv("TEXT_AI_THRESHOLD", 0.5))
    IMAGE_AI_THRESHOLD: float = float(os.getenv("IMAGE_AI_THRESHOLD", 0.5))

    MAX_TEXT_LENGTH: int = int(os.getenv("MAX_TEXT_LENGTH", 512))


settings = Settings()