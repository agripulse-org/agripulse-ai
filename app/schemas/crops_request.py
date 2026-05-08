from pydantic import BaseModel, Field

from app.schemas.soil_type import SoilType


class CropsRequest(BaseModel):
    nitrogen: float = Field(..., ge=0, le=140, description="Nitrogen (N) content in the soil. Unit: mg/kg. Typical range: 0–140.")
    temperature: float = Field(..., ge=-10, le=50, description="Average ambient temperature. Unit: °C. Accepted range: -10 to 50.")
    humidity: float = Field(..., ge=0, le=100, description="Relative humidity of the air. Unit: %. Accepted range: 0–100.")
    ph: float = Field(..., ge=0, le=14, description="Soil pH level. Accepted range: 0 (very acidic) to 14 (very alkaline). Neutral is 7.")
    moisture: float = Field(..., ge=0, le=100, description="Soil moisture content. Unit: %. Accepted range: 0–100%.")
    soil_type: SoilType = Field(..., description="Soil texture classification")
