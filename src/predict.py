# src/predict.py
import joblib
import pandas as pd
from .feature_extractor import extract_features_from_url
import os

# Lazy load model — only load when needed
_model = None

def get_model():
    global _model
    if _model is None:
        model_path = os.path.join(os.path.dirname(__file__), "..", "models", "phish_detector_pipeline.joblib")
        try:
            _model = joblib.load(model_path)
        except Exception as e:
            raise RuntimeError(f"Failed to load model: {e}")
    return _model

def predict_url(url: str):
    features = extract_features_from_url(url)
    if features is None:
        raise ValueError("Feature extraction failed")

    df = pd.DataFrame([features])
    model = get_model()
    prediction = model.predict(df)[0]
    return "Phishing 🚨" if prediction == 1 else "Safe ✅"