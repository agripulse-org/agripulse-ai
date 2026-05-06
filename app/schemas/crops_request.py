"""Pydantic v2 request schema for the crop recommendation endpoint with field-level validation."""

from pydantic import BaseModel, Field


class CropsRequest(BaseModel):
    nitrogen: float = Field(..., ge=0, le=140, description="Nitrogen content in soil (mg/kg)")
    phosphorus: float = Field(..., ge=0, le=145, description="Phosphorus content in soil (mg/kg)")
    potassium: float = Field(..., ge=0, le=205, description="Potassium content in soil (mg/kg)")
    temperature: float = Field(..., ge=-10, le=50, description="Average temperature in Celsius")
    humidity: float = Field(..., ge=0, le=100, description="Relative humidity percentage")
    ph: float = Field(..., ge=0, le=14, description="Soil pH level")
    rainfall: float = Field(..., ge=0, le=300, description="Annual rainfall in mm")
