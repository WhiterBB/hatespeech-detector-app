from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F
from typing import Tuple
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_CACHE_DIR = os.path.join(BASE_DIR, "..", "model_cache")

# Load the model and tokenizer
model_path = "WhiterBB/multilingual-hatespeech-detection"
print(f"🔍 Loading model from: {model_path}")
tokenizer = AutoTokenizer.from_pretrained(model_path, cache_dir=MODEL_CACHE_DIR)
model = AutoModelForSequenceClassification.from_pretrained(model_path, cache_dir=MODEL_CACHE_DIR)

# Prepare the model for inference
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()

# Classes for the model
id2label = {
    0: "non-hate",
    1: "hate"
}

def predict_texts(texts: list[str]) -> list[tuple[str, float]]:
    """
    Batch prediction for a list of texts.
    Returns a list of tuples: (label, confidence)
    """
    # Tokenize the input texts
    inputs = tokenizer(
        texts,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    )
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
        probs = F.softmax(outputs.logits, dim=-1)  

    results = []
    for p in probs:
        pred_class = torch.argmax(p).item()
        label = id2label[pred_class]
        confidence = p[pred_class].item()
        results.append((label, confidence))

    return results

