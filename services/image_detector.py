import torch
from transformers import AutoImageProcessor, AutoModel
from PIL import Image
import requests
from io import BytesIO
import base64
from models.image_head import ImageClassifierHead
from services.config import settings

class ImageDetector:

    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        self.processor = AutoImageProcessor.from_pretrained(settings.IMAGE_MODEL_NAME)
        self.backbone = AutoModel.from_pretrained(settings.IMAGE_MODEL_NAME).to(self.device)
        self.backbone.eval()

        self.classifier_head = ImageClassifierHead().to(self.device)

        # Load trained head weights if available
        # self.classifier_head.load_state_dict(torch.load("image_head.pt"))

        self.classifier_head.eval()

    def _load_image(self, image_input: str):

        if image_input.startswith("http"):
            response = requests.get(image_input)
            image = Image.open(BytesIO(response.content)).convert("RGB")
        else:
            image = Image.open(BytesIO(base64.b64decode(image_input))).convert("RGB")

        return image

    def _predict_image(self, image: Image.Image):

        inputs = self.processor(images=image, return_tensors="pt").to(self.device)

        with torch.no_grad():
            outputs = self.backbone(**inputs)
            embedding = outputs.last_hidden_state[:, 0, :]
            logits = self.classifier_head(embedding)
            probs = torch.softmax(logits, dim=1)

        return probs[0][1].item()  # probability of AI

    def analyze(self, images: list):

        results = []

        for idx, image_input in enumerate(images):

            try:
                image = self._load_image(image_input)
                ai_prob = self._predict_image(image)

                results.append({
                    "image_index": idx,
                    "ai_probability_percent": round(ai_prob * 100, 2),
                    "is_ai": ai_prob > settings.IMAGE_AI_THRESHOLD
                })

            except Exception as e:
                results.append({
                    "image_index": idx,
                    "error": str(e)
                })

        return results