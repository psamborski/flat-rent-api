from typing import List, Optional
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from database.FlatSchema import FlatSchema


# Pydantic model for Flat data validation
class FlatCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=150)
    description: Optional[str] = Field(None, max_length=1000)
    address: str = Field(..., max_length=200)
    coordinates: str = Field(..., pattern=r"^-?\d+(\.\d+)?,-?\d+(\.\d+)?$")  # Validate coordinates format (e.g., "52.2297,21.0122")
    floor: Optional[int] = Field(None, ge=0)
    rooms_number: int = Field(..., ge=0)
    square: float = Field(..., gt=0)
    price: float = Field(..., ge=0)
    currency: str = Field(default="PLN", max_length=10)
    city_id: int = Field(..., gt=0)
    district_id: int = Field(..., gt=0)


class FlatResource:
    def __init__(self, db: Session):
        """
        Initialize the FlatResource with a database session.

        :param db: SQLAlchemy database session.
        """
        self.db = db

    def get_all_flats(self) -> List[FlatSchema]:
        """
        Retrieve all flats from the database.

        :return: A list of FlatSchema instances representing all flats in the database.
        """
        return self.db.query(FlatSchema).all()

    def get_flat_by_id(self, flat_id: int) -> Optional[FlatSchema]:
        """
        Retrieve a single flat by its ID.

        :param flat_id: The ID of the flat to retrieve.
        :return: A FlatSchema instance representing the flat, or None if no flat is found.
        """
        return self.db.query(FlatSchema).filter(FlatSchema.id == flat_id).first()

    def get_flats_by_district(self, district_id: int) -> List[FlatSchema]:
        """
        Retrieve all flats in a specific district.

        :param district_id: The ID of the district to filter flats by.
        :return: A list of FlatSchema instances representing flats in the specified district.
        """
        return self.db.query(FlatSchema).filter(FlatSchema.district_id == district_id).all()

    def get_flats_by_city(self, city_id: int) -> List[FlatSchema]:
        """
        Retrieve all flats in a specific city.

        :param city_id: The ID of the city to filter flats by.
        :return: A list of FlatSchema instances representing flats in the specified city.
        """
        return self.db.query(FlatSchema).filter(FlatSchema.city_id == city_id).all()

    def create_flat(self, flat_data: FlatCreate) -> FlatSchema:
        """
        Create a new flat in the database.

        :param flat_data: A FlatCreate instance containing the data for the new flat.
        :return: A FlatSchema instance representing the newly created flat.
        """
        flat = FlatSchema(
            title=flat_data.title,
            description=flat_data.description,
            address=flat_data.address,
            coordinates=f"POINT({flat_data.coordinates})",  # Convert coordinates to WKT format
            floor=flat_data.floor,
            rooms_number=flat_data.rooms_number,
            square=flat_data.square,
            price=flat_data.price,
            currency=flat_data.currency,
            city_id=flat_data.city_id,
            district_id=flat_data.district_id,
        )
        self.db.add(flat)
        self.db.commit()
        self.db.refresh(flat)
        return flat