"""Pydantic v2 response schema for the crop recommendation endpoint."""

from pydantic import BaseModel, Field
from typing import List


class CropRecommendation(BaseModel):
    crop: str
    recommendation_score: float = Field(..., ge=0.0, le=1.0)


class CropsResponse(BaseModel):
    recommendations: List[CropRecommendation]
