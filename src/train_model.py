import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import joblib

from .feature_extractor import FEATURE_COLUMNS  # your features

# Load dataset
df = pd.read_csv("../data/Phishing_URL.csv")

X = df[FEATURE_COLUMNS].astype(float)
y = df["label"].astype(int)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, stratify=y, test_size=0.20, random_state=42
)

# Train model
pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("clf", RandomForestClassifier(random_state=42))
])

pipeline.fit(X_train, y_train)

# Save model
joblib.dump(pipeline, "models/phish_detector_pipeline.joblib")
print("✅ Model trained and saved in models/")
