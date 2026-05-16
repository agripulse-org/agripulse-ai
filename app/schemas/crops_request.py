from pydantic import BaseModel, Field

from app.schemas.soil_type import SoilType


class CropsRequest(BaseModel):
    model_config = {"json_schema_extra": {"example": {
        "temperature": 16.0,
        "humidity": 67.0,
        "moisture": 40.0,
        "soil_type": "loamy",
        "nitrogen": 155.0,
        "ph": 6.6,
    }}}

    temperature: float = Field(
        ..., ge=2, le=35,
        description="Growing-season average temperature (°C). Typical range: 9–26.",
    )
    humidity: float = Field(
        ..., ge=20, le=98,
        description="Relative air humidity (%). Typical range: 42–78.",
    )
    moisture: float = Field(
        ..., ge=8, le=85,
        description="Soil moisture content (%). Typical range: 22–64.",
    )
    soil_type: SoilType = Field(..., description="Soil texture classification.")
    nitrogen: float = Field(
        ..., ge=10, le=400,
        description="Total soil nitrogen (cg/kg). Typical range: 65–215.",
    )
    ph: float = Field(
        ..., ge=3.5, le=9.5,
        description="Soil pH. Typical range: 5.7–7.1.",
    )
