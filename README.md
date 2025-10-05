# 🎣 Phishing Website Detector

A machine learning-powered phishing detection system that extracts features from URLs and web pages to identify potential phishing attempts. The project includes a FastAPI scoring endpoint, comprehensive feature extraction, model training pipeline, and a browser extension prototype.

## 🚀 Features

- **Real-time URL Analysis**: Extract behavioral and structural features from URLs
- **REST API**: FastAPI endpoint for easy integration
- **ML Pipeline**: Pre-trained model with scikit-learn pipeline
- **Browser Extension**: Prototype extension for in-browser protection
- **Comprehensive Feature Set**: Analyzes URL structure, domain properties, and page content

## 📁 Project Structure

```
phishing-detector/
├── src/
│   ├── api.py                    # FastAPI server with /predict endpoint
│   ├── predict.py                # Prediction helpers and model loading
│   ├── feature_extractor.py      # Feature extraction logic
│   └── train_model.py            # Model training script
├── models/
│   └── phish_detector_pipeline.joblib  # Trained model (generated)
├── data/
│   └── Phishing_URL.csv          # Training dataset (not in repo)
├── notebooks/
│   └── phish_detector_full_notebook.ipynb  # Research & experiments
├── extension/                    # Browser extension prototype
├── test_api.py                   # API tests
├── requirements.txt              # Python dependencies
├── .gitignore                    # Excludes models and data
└── README.md
```

## 🛠️ Setup

### Prerequisites

- Python 3.8+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/phishing-detector.git
   cd phishing-detector
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Prepare the model**
   
   Ensure you have the trained model at `models/phish_detector_pipeline.joblib`. If not, train a new model (see [Training](#-training-the-model) section).

## 🚀 Usage

### Starting the API Server

Run the FastAPI server:

```bash
uvicorn src.api:app --reload
```

The API will be available at `http://localhost:8000`. Visit `http://localhost:8000/docs` for interactive API documentation.

### Making Predictions via API

**cURL example:**

```bash
curl -X POST "http://localhost:8000/predict/" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://example.com"}'
```

**Response:**

```json
{
  "url": "https://example.com",
  "prediction": "Safe ✅",
  "confidence": 0.95
}
```

### Using the Python Module

```python
from src.predict import predict_url

result = predict_url("https://suspicious-site.com")
print(result)  # "Phishing 🚨" or "Safe ✅"
```

## 🎓 Training the Model

To train or retrain the model with your own dataset:

1. Place your dataset at `data/Phishing_URL.csv`
2. Run the training script:

```bash
python src/train_model.py
```

This will:
- Load and preprocess the dataset
- Train a classification pipeline
- Save the model to `models/phish_detector_pipeline.joblib`

**Expected CSV format:**

The dataset should contain URL features as columns (defined in `FEATURE_COLUMNS`) and a target column indicating phishing/legitimate labels.

## 🧪 Testing

Run the test suite:

```bash
pytest test_api.py
```

## 🧩 Browser Extension

A prototype browser extension is included in the `extension/` directory. This extension allows users to check URLs directly from their browser.

**Installation (Chrome/Edge):**

1. Open `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select the `extension/` directory

## 📊 Features Extracted

The feature extractor (`src/feature_extractor.py`) analyzes:

- **URL Structure**: Length, special characters, subdomain count
- **Domain Properties**: Age, WHOIS data, SSL certificate status
- **Content Analysis**: HTML structure, forms, external links
- **Behavioral Patterns**: Redirects, JavaScript usage, iframe presence

See `FEATURE_COLUMNS` in `src/feature_extractor.py` for the complete feature list.

## 📓 Research & Development

The `notebooks/phish_detector_full_notebook.ipynb` contains:
- Feature engineering experiments
- Model selection and evaluation
- Performance metrics and visualizations
- Serialization of scalers and feature columns

## ⚠️ Important Notes

- **Live Requests**: Feature extraction makes real HTTP requests to analyze pages. Use responsibly and be aware of rate limits.
- **Privacy**: Never send sensitive URLs to untrusted servers.
- **Accuracy**: No phishing detector is 100% accurate. Use this as one layer in a defense-in-depth strategy.

## 🔒 Security Considerations

- The model and data files are excluded from version control (see `.gitignore`)
- Always validate and sanitize input URLs
- Consider implementing rate limiting for production deployments
- Keep dependencies updated for security patches

## 📦 Dependencies

Core dependencies (see `requirements.txt` for complete list):

- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `scikit-learn` - Machine learning
- `pandas` - Data manipulation
- `requests` - HTTP requests
- `beautifulsoup4` - HTML parsing

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Dataset source: [Add your dataset source]
- Inspired by research in phishing detection and URL analysis

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Disclaimer**: This tool is for educational and research purposes. Always exercise caution when visiting unfamiliar websites.
