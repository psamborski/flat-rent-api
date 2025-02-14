from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import SCHEMA
from database.database import Base


class AmenitySchema(Base):
    """
    Represents the 'amenities' table in the database.
    Stores information about amenities that can be associated with flats.
    """
    __tablename__ = "amenities"
    __table_args__ = {'schema': SCHEMA}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), index=True)  # Amenity name, indexed for faster queries

    # Relationships
    flats = relationship("FlatSchema", secondary=f"{SCHEMA}.flat_amenities",
                         back_populates="amenities")  # Many-to-many relationship with flats

    def __repr__(self):
        return f"<Amenity {self.name} - id {self.id}>"
