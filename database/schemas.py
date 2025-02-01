from geoalchemy2 import Geometry
from sqlalchemy import Column, Integer, String, Float, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship

from database.database import Base

SCHEMA = "flat_rent_api"


class CitySchema(Base):
    __tablename__ = "cities"
    __table_args__ = {'schema': SCHEMA}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    boundaries = Column(Geometry(geometry_type='POLYGON', srid=4326))
    country = Column(String, index=True)

    # Relationship with flats: if a city is deleted, all related flats will also be deleted
    flats = relationship("FlatSchema", back_populates="city", cascade="all, delete-orphan")
    # Relationship with districts: if a city is deleted, all related districts will also be deleted
    districts = relationship("DistrictSchema", back_populates="city", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<City {self.name} - id {self.id}>"


class DistrictSchema(Base):
    __tablename__ = "districts"
    __table_args__ = {'schema': SCHEMA}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    boundaries = Column(Geometry(geometry_type='POLYGON', srid=4326))
    city_id = Column(Integer, ForeignKey(f"{SCHEMA}.cities.id", ondelete="CASCADE"),
                     nullable=False)  # ON DELETE CASCADE

    # Relationship with flats: if a district is deleted, all related flats will also be deleted
    flats = relationship("FlatSchema", back_populates="district", cascade="all, delete-orphan")

    def __repr__(self):
        return (f"<District {self.name} - id {self.id}>"
                f"City: {self.city_id}")


class FlatSchema(Base):
    __tablename__ = "flats"
    __table_args__ = (
        {'schema': SCHEMA},
        CheckConstraint('price >= 0', name='check_price_positive'),  # Price cannot be negative
        CheckConstraint('square > 0', name='check_square_positive'),  # Square footage must be positive
        CheckConstraint('rooms_number >= 0', name='check_rooms_number_positive'),  # Number of rooms cannot be negative
    )

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    address = Column(String)
    coordinates = Column(Geometry(geometry_type="POINT", srid=4326), nullable=False)
    floor = Column(Integer)
    rooms_number = Column(Integer)
    square = Column(Float)
    price = Column(Float, nullable=False)  # per month
    currency = Column(String, default="PLN", nullable=False)
    city_id = Column(Integer, ForeignKey(f"{SCHEMA}.cities.id", ondelete="CASCADE"), nullable=False, index=True)
    district_id = Column(Integer, ForeignKey(f"{SCHEMA}.districts.id", ondelete="CASCADE"), nullable=False, index=True)

    city = relationship("CitySchema", back_populates="flats")
    district = relationship("DistrictSchema", back_populates="flats")
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
                f"\nCity: {self.city.name} - id {self.city.id}"
                f"\nDistrict: {self.district.name} - id {self.district.id}")


class AmenitySchema(Base):
    __tablename__ = "amenities"
    __table_args__ = {'schema': SCHEMA}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    flats = relationship("FlatSchema", secondary=f"{SCHEMA}.flat_amenities", back_populates="amenities")

    def __repr__(self):
        return f"<Amenity {self.name} - id {self.id}>"


class FlatAmenitySchema(Base):
    __tablename__ = "flat_amenities"
    __table_args__ = {'schema': SCHEMA}

    flat_id = Column(Integer, ForeignKey(f"{SCHEMA}.flats.id", ondelete="CASCADE"),
                     primary_key=True)
    amenity_id = Column(Integer, ForeignKey(f"{SCHEMA}.amenities.id", ondelete="CASCADE"),
                        primary_key=True)

    def __repr__(self):
        return f"<FlatAmenity flat {self.flat_id} - amenity {self.amenity_id}>"
