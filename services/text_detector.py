import torch
import nltk
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np
from services.config import settings

nltk.download("punkt")
from nltk.tokenize import sent_tokenize


class TextDetector:

    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.tokenizer = AutoTokenizer.from_pretrained(
            settings.TEXT_MODEL_NAME
        )

        self.model = AutoModelForSequenceClassification.from_pretrained(
            settings.TEXT_MODEL_NAME
        ).to(self.device)

        self.model.eval()

    def _score_text(self, text: str):
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=512
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model(**inputs)

        probs = torch.softmax(outputs.logits, dim=1)
        ai_prob = probs[0][1].item()  # Assuming label 1 = AI

        return ai_prob

    def analyze(self, text: str):

        overall_ai_prob = self._score_text(text)

        sentences = sent_tokenize(text)

        sentence_scores = []

        for sentence in sentences:
            if len(sentence.split()) < 5:
                continue

            score = self._score_text(sentence)
            sentence_scores.append((sentence, score))

        sentence_scores.sort(key=lambda x: x[1], reverse=True)

        top_ai_sentences = [
            {
                "sentence": s,
                "ai_probability": round(p * 100, 2)
            }
            for s, p in sentence_scores[:3] if p > settings.TEXT_AI_THRESHOLD
        ]

        return {
            "ai_probability_percent": round(overall_ai_prob * 100, 2),
            "top_ai_sentences": top_ai_sentences
        }