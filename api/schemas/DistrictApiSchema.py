from typing import Dict, Any
from pydantic import BaseModel, Field

from api.schemas.CityApiSchema import CityParentResponse


class DistrictCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, description="City name")
    boundaries: Dict[str, Any] = Field(..., description="Geographic boundaries in GeoJSON format")
    city_id: int = Field(..., max_length=200, description="City ID.")

class DistrictResponse(BaseModel):
    id: int
    name: str
    boundaries: Dict[str, Any]
    city: CityParentResponse

    class Config:
        orm_mode = True

class DistrictChildResponse(BaseModel):
    id: int
    name: str
    boundaries: Dict[str, Any]

    class Config:
        orm_mode = True