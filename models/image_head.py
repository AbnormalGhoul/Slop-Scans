import torch
import torch.nn as nn


class ImageClassifierHead(nn.Module):
    def __init__(self, embedding_dim=384):
        super().__init__()
        self.classifier = nn.Sequential(
            nn.Linear(embedding_dim, 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, 2)
        )

    def forward(self, x):
        return self.classifier(x)