import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoConfig, AutoModel, PreTrainedModel
from config import settings


class DesklibAIDetectionModel(PreTrainedModel):
    config_class = AutoConfig

    def __init__(self, config):
        super().__init__(config)

        self.model = AutoModel.from_config(config)
        self.classifier = nn.Linear(config.hidden_size, 1)

        self.post_init()

    def forward(self, input_ids, attention_mask=None):
        outputs = self.model(
            input_ids=input_ids,
            attention_mask=attention_mask
        )

        last_hidden_state = outputs[0]

        # Mean Pooling
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(
            last_hidden_state.size()
        ).float()

        sum_embeddings = torch.sum(
            last_hidden_state * input_mask_expanded, dim=1
        )

        sum_mask = torch.clamp(
            input_mask_expanded.sum(dim=1), min=1e-9
        )

        pooled_output = sum_embeddings / sum_mask

        logits = self.classifier(pooled_output)

        return {"logits": logits}


class TextAIDetector:
    def __init__(self):
        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )

        self.tokenizer = AutoTokenizer.from_pretrained(
            settings.TEXT_MODEL_NAME
        )

        self.model = DesklibAIDetectionModel.from_pretrained(
            settings.TEXT_MODEL_NAME
        )

        self.model.to(self.device)
        self.model.eval()

    def predict(self, text: str):
        encoded = self.tokenizer(
            text,
            padding='max_length',
            truncation=True,
            max_length=settings.MAX_TEXT_LENGTH,
            return_tensors='pt'
        )

        input_ids = encoded["input_ids"].to(self.device)
        attention_mask = encoded["attention_mask"].to(self.device)

        with torch.no_grad():
            outputs = self.model(
                input_ids=input_ids,
                attention_mask=attention_mask
            )

        logits = outputs["logits"]
        probability = torch.sigmoid(logits).item()

        return {
            "ai_probability": probability,
            "is_ai_generated": probability >= settings.TEXT_AI_THRESHOLD
        }


text_detector = TextAIDetector()