from sqlalchemy import Column, Integer, ForeignKey

from database import SCHEMA
from database.database import Base


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
