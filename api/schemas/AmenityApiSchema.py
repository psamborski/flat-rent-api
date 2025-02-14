from pydantic import BaseModel


class AmenityCreate(BaseModel):
    name: str

class AmenityResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
