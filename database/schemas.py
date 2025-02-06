from geoalchemy2 import Geometry
from sqlalchemy import Column, Integer, String, Float, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship

from database.database import Base

SCHEMA = "flat_rent_api"  # Database schema name for organizing tables


class CitySchema(Base):
    """
    Represents the 'cities' table in the database.
    Stores information about cities, including their boundaries and associated country.
    """
    __tablename__ = "cities"  # Table name
    __table_args__ = {'schema': SCHEMA}  # Specifies the schema for this table

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)  # City name, indexed for faster queries
    boundaries = Column(Geometry(geometry_type='POLYGON', srid=4326))  # Geographic boundaries of the city
    country = Column(String, index=True)  # Country name, indexed for faster queries

    # Relationships
    flats = relationship("FlatSchema", back_populates="city", cascade="all, delete-orphan")  # One-to-many relationship with flats
    districts = relationship("DistrictSchema", back_populates="city", cascade="all, delete-orphan")  # One-to-many relationship with districts

    def __repr__(self):
        return f"<City {self.name} - id {self.id}>"  # String representation of the object


class DistrictSchema(Base):
    """
    Represents the 'districts' table in the database.
    Stores information about districts, including their boundaries and associated city.
    """
    __tablename__ = "districts"
    __table_args__ = {'schema': SCHEMA}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)  # District name, indexed for faster queries
    boundaries = Column(Geometry(geometry_type='POLYGON', srid=4326))  # Geographic boundaries of the district
    city_id = Column(Integer, ForeignKey(f"{SCHEMA}.cities.id", ondelete="CASCADE"), nullable=False)

    # Relationships
    flats = relationship("FlatSchema", back_populates="district", cascade="all, delete-orphan")  # One-to-many relationship with flats

    def __repr__(self):
        return f"<District {self.name} - id {self.id}> City: {self.city_id}"  # String representation of the object


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
        CheckConstraint('rooms_number >= 0', name='check_rooms_number_positive'),  # Ensures rooms number is non-negative
    )

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)  # Title of the flat listing
    description = Column(String)
    address = Column(String)  # Address of the flat
    coordinates = Column(Geometry(geometry_type="POINT", srid=4326), nullable=False)  # Geographic coordinates of the flat
    floor = Column(Integer)
    rooms_number = Column(Integer)
    square = Column(Float)  # Square footage of the flat
    price = Column(Float, nullable=False)  # Monthly rental price
    currency = Column(String, default="PLN", nullable=False)  # Currency of the price (default: PLN)
    city_id = Column(Integer, ForeignKey(f"{SCHEMA}.cities.id", ondelete="CASCADE"), nullable=False, index=True)
    district_id = Column(Integer, ForeignKey(f"{SCHEMA}.districts.id", ondelete="CASCADE"), nullable=False, index=True)

    # Relationships
    city = relationship(
        "CitySchema", back_populates="flats")  # Many-to-one relationship with cities
    district = relationship(
        "DistrictSchema", back_populates="flats")  # Many-to-one relationship with districts
    amenities = relationship(
        "AmenitySchema", secondary=f"{SCHEMA}.flat_amenities", back_populates="flats")  # Many-to-many relationship with amenities

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
    """
    Represents the 'amenities' table in the database.
    Stores information about amenities that can be associated with flats.
    """
    __tablename__ = "amenities"
    __table_args__ = {'schema': SCHEMA}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)  # Amenity name, indexed for faster queries

    # Relationships
    flats = relationship("FlatSchema", secondary=f"{SCHEMA}.flat_amenities", back_populates="amenities")  # Many-to-many relationship with flats

    def __repr__(self):
        return f"<Amenity {self.name} - id {self.id}>"


class FlatAmenitySchema(Base):
    """
    Represents the 'flat_amenities' table in the database.
    Acts as a join table for the many-to-many relationship between flats and amenities.
    """
    __tablename__ = "flat_amenities"
    __table_args__ = {'schema': SCHEMA}

    flat_id = Column(Integer, ForeignKey(f"{SCHEMA}.flats.id", ondelete="CASCADE"), primary_key=True)
    amenity_id = Column(Integer, ForeignKey(f"{SCHEMA}.amenities.id", ondelete="CASCADE"), primary_key=True)

    def __repr__(self):
        return f"<FlatAmenity flat {self.flat_id} - amenity {self.amenity_id}>"