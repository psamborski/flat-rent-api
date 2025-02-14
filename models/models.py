from pydantic import BaseModel
from typing import List, Optional

# Base model for City
class CityBase(BaseModel):
    name: str
    country: str

class CityCreate(CityBase):
    pass

class City(CityBase):
    id: int

    class Config:
        orm_mode = True # = treat SQLAlchemy objects as dicts

# Base model for Amenity
class AmenityBase(BaseModel):
    name: str

class AmenityCreate(AmenityBase):
    pass

class Amenity(AmenityBase):
    id: int

    class Config:
        orm_mode = True

# Base model for Flat
class FlatBase(BaseModel):
    title: str
    description: str
    address: str
    latitude: float
    longitude: float
    city_id: int
    floor: int
    rooms_number: int
    square: float
    price: float
    currency: str
    amenities_ids: List[int]  # List of amenity ids

class FlatCreate(FlatBase):
    pass

class Flat(FlatBase):
    id: int
    city: City
    amenities: List[Amenity]

    class Config:
        orm_mode = True