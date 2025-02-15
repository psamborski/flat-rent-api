from typing import Dict, Any
from pydantic import BaseModel, Field

from api.schemas.CityApiSchema import CityParentResponse


class DistrictCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)  # District name, required, 1-200 characters
    boundaries: Dict[str, Any] = Field(..., description="Geographic boundaries in GeoJSON format")  # GeoJSON format
    city_id: int = Field(..., gt=0,
                         description="ID of the city associated with the district")  # City ID, must be greater than 0

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