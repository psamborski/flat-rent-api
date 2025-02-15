from typing import List, Optional, Dict, Any

from pydantic import BaseModel, Field

from api.schemas.AmenityApiSchema import AmenityResponse
from api.schemas.CityApiSchema import CityParentResponse
from api.schemas.DistrictApiSchema import DistrictChildResponse


class FlatCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=150)
    description: str = Field(..., min_length=1, max_length=1000)
    address: str = Field(..., max_length=200)
    city_id: int = Field(..., gt=0)
    district_id: int = Field(..., gt=0)
    floor: Optional[int] = Field(None, ge=0)
    rooms_number: int = Field(..., ge=0)
    square: float = Field(..., gt=0)
    price: float = Field(..., ge=0)
    currency: str = Field(default="PLN", max_length=10)
    amenities_ids: List[int] = Field(default_factory=lambda: [], description="List of amenities IDs")
    coordinates: Dict[str, Any] = Field(..., description="Geographic coordinates in GeoJSON format")


class FlatUpdate(BaseModel):
    id: int = Field(..., gt=0)
    title: Optional[str] = Field(None, min_length=1, max_length=150)
    description: Optional[str] = Field(None, min_length=1, max_length=1000)
    address: Optional[str] = Field(None, max_length=200)
    city_id: Optional[int] = Field(None, gt=0)
    district_id: Optional[int] = Field(None, gt=0)
    floor: Optional[int] = Field(None, ge=0)
    rooms_number: Optional[int] = Field(None, ge=0)
    square: Optional[float] = Field(None, gt=0)
    price: Optional[float] = Field(None, ge=0)
    currency: Optional[str] = Field(default="PLN", max_length=10)
    amenities_ids: Optional[List[int]] = Field(default_factory=lambda: [], description="List of amenities IDs")
    coordinates: Optional[Dict[str, Any]] = Field(None, description="Geographic coordinates in GeoJSON format")


class FlatResponse(BaseModel):
    id: int
    title: str
    description: str
    address: str
    price: float
    currency: str
    floor: Optional[int]
    rooms_number: int
    square: float
    amenities: List[AmenityResponse] = []
    coordinates: Dict[str, Any]
    city: CityParentResponse
    district: DistrictChildResponse

    class Config:
        orm_mode = True
