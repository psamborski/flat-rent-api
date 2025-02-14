from typing import Dict, Any, List
from pydantic import BaseModel, Field

from api.schemas.DistrictApiSchema import DistrictChildResponse


class CityCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, description="City name")
    boundaries: Dict[str, Any] = Field(..., description="Geographic boundaries in GeoJSON format")
    country: str = Field(..., max_length=200, description="Country name")

class CityResponse(BaseModel):
    id: int
    name: str
    boundaries: Dict[str, Any]
    country: str
    districts: List[DistrictChildResponse] = []

    class Config:
        orm_mode = True

class CityParentResponse(BaseModel):
    id: int
    name: str
    boundaries: Dict[str, Any]
    country: str

    class Config:
        orm_mode = True