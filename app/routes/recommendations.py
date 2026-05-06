"""Route handler for POST /api/recommendations/crops; delegates inference to the ML service."""

from fastapi import APIRouter
from app.schemas.crops_request import CropsRequest
from app.schemas.crops_response import CropsResponse
from app.services.ml_service import get_crop_recommendations

router = APIRouter()


@router.post("/recommendations/crops", response_model=CropsResponse)
def recommend_crops(request: CropsRequest) -> CropsResponse:
    return get_crop_recommendations(request)
