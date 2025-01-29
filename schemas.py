from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    country = Column(String)

    def __repr__(self):
        return f"<City {self.name} - id {self.id}>"


class Amenity(Base):
    __tablename__ = "amenities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    def __repr__(self):
        return f"<Amenity {self.name} - id {self.id}>"

class Flat(Base):
    __tablename__ = "flats"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    currency = Column(String)
    coordinates = Column(String)  # Store coordinates as a string (e.g., "latitude,longitude")
    city_id = Column(Integer, ForeignKey("cities.id"))

    city = relationship("City", back_populates="flats")
    amenities = relationship("Amenity", secondary="flat_amenities", back_populates="flats")

    def __repr__(self):
        return f"<Flat {self.title} - id {self.id}>"


class FlatAmenity(Base):
    __tablename__ = "flat_amenities"

    flat_id = Column(Integer, ForeignKey("flats.id", ondelete="CASCADE"), primary_key=True)
    amenity_id = Column(Integer, ForeignKey("amenities.id", ondelete="CASCADE"), primary_key=True)

    def __repr__(self):
        return f"<FlatAmenity flat {self.flat_id} - amenity {self.amenity_id}>"


# Establish a relationship back to the flats in Amenity class
Amenity.flats = relationship("Flat", secondary="flat_amenities", back_populates="amenities")

# Establish a relationship back to the flats in City class
City.flats = relationship("Flat", back_populates="city")