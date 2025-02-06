from geoalchemy2 import Geometry
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import SCHEMA
from database.database import Base


class CitySchema(Base):
    """
    Represents the 'cities' table in the database.
    Stores information about cities, including their boundaries and associated country.
    """
    __tablename__ = "cities"  # Table name
    __table_args__ = {'schema': SCHEMA}  # Specifies the schema for this table

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), index=True)  # City name, indexed for faster queries
    boundaries = Column(Geometry(geometry_type='POLYGON', srid=4326))  # Geographic boundaries of the city
    country = Column(String(200), index=True)  # Country name, indexed for faster queries

    # Relationships
    flats = relationship("FlatSchema", back_populates="city",
                         cascade="all, delete-orphan")  # One-to-many relationship with flats
    districts = relationship("DistrictSchema", back_populates="city",
                             cascade="all, delete-orphan")  # One-to-many relationship with districts

    def __repr__(self):
        return f"<City {self.name} - id {self.id}>"  # String representation of the object
