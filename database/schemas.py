from geoalchemy2 import Geography
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from database.database import Base

SCHEMA = "flat_rent_api"

class CitySchema(Base):
    __tablename__ = "cities"
    __table_args__ = {'schema': SCHEMA}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    country = Column(String)

    flats = relationship("FlatSchema", back_populates="city")

    def __repr__(self):
        return f"<City {self.name} - id {self.id}>"


class AmenitySchema(Base):
    __tablename__ = "amenities"
    __table_args__ = {'schema': SCHEMA}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    flats = relationship("FlatSchema", secondary=f"{SCHEMA}.flat_amenities", back_populates="amenities")

    def __repr__(self):
        return f"<Amenity {self.name} - id {self.id}>"


class FlatSchema(Base):
    __tablename__ = "flats"
    __table_args__ = {'schema': SCHEMA}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String)
    address = Column(String)
    coordinates = Column(Geography(geometry_type="POINT", srid=4326), nullable=False)
    floor = Column(Integer)
    rooms_number = Column(Integer)
    square = Column(Float)
    price = Column(Float, nullable=False)  # per month
    currency = Column(String, default="PLN", nullable=False)
    city_id = Column(Integer, ForeignKey(f"{SCHEMA}.cities.id"), nullable=False)  # Pełna ścieżka do tabeli

    city = relationship("CitySchema", back_populates="flats")
    amenities = relationship("AmenitySchema", secondary=f"{SCHEMA}.flat_amenities", back_populates="flats")

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
                f"\nCity: {self.city.name} - id {self.city.id}")


class FlatAmenitySchema(Base):
    __tablename__ = "flat_amenities"
    __table_args__ = {'schema': SCHEMA}

    flat_id = Column(Integer, ForeignKey(f"{SCHEMA}.flats.id", ondelete="CASCADE"), primary_key=True)
    amenity_id = Column(Integer, ForeignKey(f"{SCHEMA}.amenities.id", ondelete="CASCADE"), primary_key=True)

    def __repr__(self):
        return f"<FlatAmenity flat {self.flat_id} - amenity {self.amenity_id}>"