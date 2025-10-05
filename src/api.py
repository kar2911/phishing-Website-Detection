# src/api.py
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
from .feature_extractor import extract_features_from_url

app = FastAPI()
model = joblib.load("models/phish_detector_pipeline.joblib")



class URLRequest(BaseModel):
    url: str

@app.post("/predict/")
def predict(request: URLRequest):
    features = extract_features_from_url(request.url)  # ← Returns list of 50 numbers
    prediction = model.predict([features])[0]  # ← No DataFrame needed!
    return {
        "url": request.url,
        "is_phishing": bool(prediction),
        "result": "Phishing 🚨" if prediction == 1 else "Safe ✅"
    }