import requests
from config import settings

class ImageAIDetector:
    def __init__(self):
        if not settings.SIGHTENGINE_API_USER or not settings.SIGHTENGINE_API_SECRET:
            raise ValueError("Sightengine API credentials are missing.")

        self.api_user = settings.SIGHTENGINE_API_USER
        self.api_secret = settings.SIGHTENGINE_API_SECRET
        self.endpoint = "https://api.sightengine.com/1.0/check.json"

    def predict_from_bytes(self, image_bytes: bytes):
        files = {
            "media": ("image.jpg", image_bytes)
        }

        data = {
            "models": "genai",
            "api_user": self.api_user,
            "api_secret": self.api_secret
        }

        response = requests.post(
            self.endpoint,
            files=files,
            data=data,
            timeout=10
        )

        result = response.json()

        if result.get("status") != "success":
            raise RuntimeError(f"Sightengine error: {result}")

        ai_score = result["type"]["ai_generated"]

        return {
            "ai_probability": ai_score,
            "is_ai_generated": ai_score >= settings.IMAGE_AI_THRESHOLD
        }

image_detector = ImageAIDetector()