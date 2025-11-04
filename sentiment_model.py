# sentiment_model.py
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F
import pandas as pd

MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment"

class SentimentModel:
    def __init__(self, device=None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        self.model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME).to(self.device)

    def score_texts(self, texts, batch_size=32):
        rows = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]
            enc = self.tokenizer(batch, padding=True, truncation=True, return_tensors="pt").to(self.device)
            with torch.no_grad():
                logits = self.model(**enc).logits
                probs = F.softmax(logits, dim=1).cpu().numpy()
            for t, p in zip(batch, probs):
                neg, neu, pos = float(p[0]), float(p[1]), float(p[2])
                score = pos - neg
                rows.append({"text": t, "negative": neg, "neutral": neu, "positive": pos, "sentiment_score": score})
        return pd.DataFrame(rows)
