from app.schemas.crop_type import CropType
from app.schemas.crops_request import CropsRequest
from app.schemas.crops_response import CropsResponse, CropRecommendation


def get_crop_recommendations(request: CropsRequest) -> CropsResponse:
    return CropsResponse(
        best_crop=CropType.WHEAT,
        recommendations=[
            CropRecommendation(crop=CropType.WHEAT, recommendation_score=0.88),
            CropRecommendation(crop=CropType.MAIZE, recommendation_score=0.72),
        ]
    )
