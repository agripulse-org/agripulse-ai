"""Integration tests for the /api/recommendations/crops and /health endpoints."""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

VALID_PAYLOAD = {
    "nitrogen": 90.0,
    "phosphorus": 42.0,
    "potassium": 43.0,
    "temperature": 20.88,
    "humidity": 82.0,
    "ph": 6.5,
    "rainfall": 202.93,
}


def test_recommend_crops_success():
    response = client.post("/api/recommendations/crops", json=VALID_PAYLOAD)
    assert response.status_code == 200
    data = response.json()
    assert "recommendations" in data
    assert len(data["recommendations"]) > 0
    first = data["recommendations"][0]
    assert "crop" in first
    assert "recommendation_score" in first
    assert 0.0 <= first["recommendation_score"] <= 1.0


def test_recommend_crops_missing_fields():
    response = client.post("/api/recommendations/crops", json={"nitrogen": 50.0})
    assert response.status_code == 422


def test_recommend_crops_out_of_range():
    payload = {**VALID_PAYLOAD, "ph": 20.0}  # ph must be 0-14
    response = client.post("/api/recommendations/crops", json=payload)
    assert response.status_code == 422


def test_recommend_crops_negative_value():
    payload = {**VALID_PAYLOAD, "humidity": -5.0}
    response = client.post("/api/recommendations/crops", json=payload)
    assert response.status_code == 422


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
