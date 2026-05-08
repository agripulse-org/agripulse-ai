from pydantic import BaseModel, Field
from typing import List

from app.schemas.crop_type import CropType


class CropRecommendation(BaseModel):
    crop: CropType
    recommendation_score: float = Field(..., ge=0.0, le=1.0)


class CropsResponse(BaseModel):
    best_crop: CropType
    recommendations: List[CropRecommendation]
