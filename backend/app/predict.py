from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F
from typing import Tuple

# Load the model and tokenizer
model_path = "WhiterBB/multilingual-hatespeech-detection"
cache_dir = "./model_cache"
print(f"🔍 Loading model from: {model_path}")
tokenizer = AutoTokenizer.from_pretrained(model_path, cache_dir=cache_dir)
model = AutoModelForSequenceClassification.from_pretrained(model_path, cache_dir=cache_dir)

# Prepare the model for inference
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()

# Classes for the model
id2label = {
    0: "non-hate",
    1: "hate"
}

def predict_text(text: str) -> Tuple[str, float]:
    """
    Predict the class of the given text
    """
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128)
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = F.softmax(logits, dim=-1).squeeze()

    pred_class = torch.argmax(probs).item()
    label = id2label[pred_class]
    confidence = probs[pred_class].item()

    return label, confidence
