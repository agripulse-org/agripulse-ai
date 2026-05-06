from app.schemas.crops_request import CropsRequest
from app.schemas.crops_response import CropsResponse, CropRecommendation


def get_crop_recommendations(request: CropsRequest) -> CropsResponse:
    return CropsResponse(
        recommendations=[
            CropRecommendation(crop="wheat", recommendation_score=0.88),
            CropRecommendation(crop="maize", recommendation_score=0.72),
        ]
    )
