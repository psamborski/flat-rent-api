from geoalchemy2 import Geometry
from sqlalchemy import Column, Integer, String, CheckConstraint, Float, ForeignKey
from sqlalchemy.orm import relationship

from database import SCHEMA
from database.database import Base


class FlatSchema(Base):
    """
    Represents the 'flats' table in the database.
    Stores information about rental flats, including their location, price, and amenities.
    """
    __tablename__ = "flats"  # Table name
    __table_args__ = (
        {'schema': SCHEMA},  # Specifies the schema for this table
        CheckConstraint('price >= 0', name='check_price_positive'),  # Ensures price is non-negative
        CheckConstraint('square > 0', name='check_square_positive'),  # Ensures square footage is positive
        CheckConstraint('rooms_number >= 0', name='check_rooms_number_positive'),
    # Ensures rooms number is non-negative
    )

    id = Column(Integer, primary_key=True)
    title = Column(String(150), nullable=False)  # Title of the flat listing
    description = Column(String(1000), nullable=False)
    address = Column(String(200))  # Address of the flat
    coordinates = Column(Geometry(geometry_type="POINT", srid=4326),
                         nullable=False)  # Geographic coordinates of the flat
    floor = Column(Integer)
    rooms_number = Column(Integer, nullable=False)
    square = Column(Float, nullable=False)  # Square footage of the flat
    price = Column(Float, nullable=False)  # Monthly rental price
    currency = Column(String(10), default="PLN", nullable=False)  # Currency of the price (default: PLN)
    city_id = Column(Integer, ForeignKey(f"{SCHEMA}.cities.id", ondelete="CASCADE"), nullable=False, index=True)
    district_id = Column(Integer, ForeignKey(f"{SCHEMA}.districts.id", ondelete="CASCADE"), nullable=False, index=True)

    # Relationships
    city = relationship(
        "CitySchema", back_populates="flats")  # Many-to-one relationship with cities
    district = relationship(
        "DistrictSchema", back_populates="flats")  # Many-to-one relationship with districts
    amenities = relationship(
        "AmenitySchema", secondary=f"{SCHEMA}.flat_amenities",
        back_populates="flats")  # Many-to-many relationship with amenities

    def __repr__(self):
        return (f"<Flat - id {self.id}>"
                f"\nTitle: {self.title}"
                f"\nDescription: {self.description}"
                f"\nPrice: {self.price} {self.currency}"
                f"\nAddress: {self.address}"
                f"\nCoordinates: {self.coordinates}"
                f"\nFloor: {self.floor}"
                f"\nRooms number: {self.rooms_number}"
                f"\nSquare: {self.square}"
                f"\nCity: {self.city.name} - id {self.city.id}"
                f"\nDistrict: {self.district.name} - id {self.district.id}")
