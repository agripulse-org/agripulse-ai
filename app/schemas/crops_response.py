from pydantic import BaseModel, Field
from typing import List

from app.schemas.crop_type import CropType


class CropScore(BaseModel):
    crop: CropType
    confidence: float = Field(..., ge=0.0, le=1.0)


class CropsResponse(BaseModel):
    recommended_crop: CropType
    confidence: float = Field(..., ge=0.0, le=1.0)
    top_3_crops: List[CropScore]
