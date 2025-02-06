from geoalchemy2 import Geometry
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import SCHEMA
from database.database import Base


class DistrictSchema(Base):
    """
    Represents the 'districts' table in the database.
    Stores information about districts, including their boundaries and associated city.
    """
    __tablename__ = "districts"
    __table_args__ = {'schema': SCHEMA}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), index=True)  # District name, indexed for faster queries
    boundaries = Column(Geometry(geometry_type='POLYGON', srid=4326))  # Geographic boundaries of the district
    city_id = Column(Integer, ForeignKey(f"{SCHEMA}.cities.id", ondelete="CASCADE"), nullable=False)

    # Relationships
    flats = relationship("FlatSchema", back_populates="district", cascade="all, delete-orphan")  # One-to-many relationship with flats

    def __repr__(self):
        return f"<District {self.name} - id {self.id}> City: {self.city_id}"  # String representation of the object