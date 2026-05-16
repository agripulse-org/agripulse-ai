"""Integration tests for the /api/recommendations/crops and /health endpoints."""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

VALID_PAYLOAD = {
    "temperature": 16.0,
    "humidity": 67.0,
    "moisture": 40.0,
    "soil_type": "loamy",
    "nitrogen": 155.0,
    "ph": 6.6,
}


def test_recommend_crops_success():
    response = client.post("/api/recommendations/crops", json=VALID_PAYLOAD)
    assert response.status_code == 200
    data = response.json()
    assert "best_crop" in data
    assert "recommendations" in data
    assert len(data["recommendations"]) == 13
    first = data["recommendations"][0]
    assert "crop" in first
    assert "recommendation_score" in first
    assert 0.0 <= first["recommendation_score"] <= 1.0
    assert data["best_crop"] == first["crop"]


def test_recommend_crops_missing_fields():
    response = client.post("/api/recommendations/crops", json={"nitrogen": 50.0})
    assert response.status_code == 422


def test_recommend_crops_invalid_soil_type():
    payload = {**VALID_PAYLOAD, "soil_type": "volcanic"}
    response = client.post("/api/recommendations/crops", json=payload)
    assert response.status_code == 422


def test_recommend_crops_out_of_range_humidity():
    payload = {**VALID_PAYLOAD, "humidity": 5.0}  # below ge=20
    response = client.post("/api/recommendations/crops", json=payload)
    assert response.status_code == 422


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
