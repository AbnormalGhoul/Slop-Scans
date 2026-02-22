import torch
import numpy as np
from transformers import AutoImageProcessor, AutoModel
from PIL import Image
from config import settings

class ImageAIDetector:
    def __init__(self):
        self.processor = AutoImageProcessor.from_pretrained(
            settings.IMAGE_MODEL_NAME
        )
        self.model = AutoModel.from_pretrained(
            settings.IMAGE_MODEL_NAME
        )
        self.model.eval()

    def predict(self, image: Image.Image):
        inputs = self.processor(images=image, return_tensors="pt")

        with torch.no_grad():
            outputs = self.model(**inputs)
            embeddings = outputs.last_hidden_state.mean(dim=1)

        embedding_np = embeddings[0].numpy()

        # Simple heuristic (placeholder logic)
        variance_score = float(np.var(embedding_np))
        normalized_score = min(variance_score, 1.0)

        return {
            "ai_probability": normalized_score,
            "is_ai_generated": normalized_score >= settings.IMAGE_AI_THRESHOLD
        }


image_detector = ImageAIDetector()