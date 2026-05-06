# AgriPulse AI — Crop Recommendation Service

An ML-powered HTTP service that recommends crops based on soil and climate conditions.

## Architecture

```
agripulse-ai/
├── app/                        # FastAPI service
│   ├── main.py                 # App entry point + /health endpoint
│   ├── routes/                 # HTTP route handlers
│   ├── schemas/                # Pydantic v2 request/response models
│   ├── services/               # ML inference layer (ml_service.py)
│   └── models/                 # Trained .pkl files (git-ignored)
├── crop-classifier/            # Standalone training pipeline
│   ├── train.py                # Train and export model
│   ├── evaluate.py             # Evaluate model on test split
│   ├── data/                   # Raw dataset (git-ignored)
│   ├── pipeline/
│   │   ├── model.py            # RandomForest / XGBoost wrapper
│   │   └── preprocessor.py     # Scaling and encoding pipeline
│   └── config.yaml             # Hyperparameters and feature list
└── tests/                      # pytest integration tests
```

**Request flow:** `POST /api/recommendations/crops` → route → `ml_service.get_crop_recommendations()` → returns ranked crop list.

The service and classifier are decoupled: train offline, drop the `.pkl` into `app/models/`, restart the service.

## Training the Model

1. Place your dataset at `crop-classifier/data/dataset.csv`.
   The CSV must contain the feature columns listed in `config.yaml` plus a `label` column.

2. Install training dependencies:
   ```bash
   pip install -r crop-classifier/requirements.txt
   ```

3. Train and export the model:
   ```bash
   cd crop-classifier
   python train.py
   ```
   The fitted pipeline is saved to `app/models/crop_classifier.pkl`.

4. Evaluate on a held-out test split:
   ```bash
   python evaluate.py
   ```

## Running the Service

### Locally with uvicorn

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Endpoints:
- `GET  /health` — liveness check
- `POST /api/recommendations/crops` — crop recommendation

Example request:
```bash
curl -X POST http://localhost:8000/api/recommendations/crops \
  -H "Content-Type: application/json" \
  -d '{
    "nitrogen": 90,
    "phosphorus": 42,
    "potassium": 43,
    "temperature": 20.88,
    "humidity": 82,
    "ph": 6.5,
    "rainfall": 202.93
  }'
```

Example response:
```json
{
  "recommendations": [
    { "crop": "wheat", "recommendation_score": 0.88 },
    { "crop": "maize", "recommendation_score": 0.72 }
  ]
}
```

### With Docker

```bash
docker build -t agripulse-ai .
docker run -p 8000:8000 agripulse-ai
```

To mount a trained model into the container:
```bash
docker run -p 8000:8000 -v $(pwd)/app/models:/app/app/models agripulse-ai
```

## Running Tests

```bash
pip install -r requirements.txt pytest httpx
pytest tests/
```

## Configuration

| File | Purpose |
|---|---|
| `.env.example` | Service environment variables |
| `crop-classifier/.env.example` | Training environment variables |
| `crop-classifier/config.yaml` | Feature list and model hyperparameters |
