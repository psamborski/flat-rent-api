from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from database.database import Base


class CitySchema(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    country = Column(String)

    def __repr__(self):
        return f"<City {self.name} - id {self.id}>"


class AmenitySchema(Base):
    __tablename__ = "amenities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    def __repr__(self):
        return f"<Amenity {self.name} - id {self.id}>"


class FlatSchema(Base):
    __tablename__ = "flats"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    address = Column(String)
    # coordinates = Column(Geography(geometry_type="POINT", srid=4326))
    # Storing as Geography POINT (latitude, longitude) POSTGRE ONLY
    latitude = Column(Float)  # Latitude of the apartment
    longitude = Column(Float)  # Longitude of the apartment
    floor = Column(Integer)
    rooms_number = Column(Integer)
    square = Column(Float)
    price = Column(Float)  # per month
    currency = Column(String, default="PLN")
    city_id = Column(Integer, ForeignKey("cities.id"))

    city = relationship("CitySchema", back_populates="flats")
    amenities = relationship("AmenitySchema", secondary="flat_amenities", back_populates="flats")

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

    flat_id = Column(Integer, ForeignKey("flats.id", ondelete="CASCADE"), primary_key=True)
    amenity_id = Column(Integer, ForeignKey("amenities.id", ondelete="CASCADE"), primary_key=True)

    def __repr__(self):
        return f"<FlatAmenity flat {self.flat_id} - amenity {self.amenity_id}>"


# Establish a relationship back to the flats in Amenity class
AmenitySchema.flats = relationship("FlatSchema", secondary="flat_amenities", back_populates="amenities")

# Establish a relationship back to the flats in City class
CitySchema.flats = relationship("FlatSchema", back_populates="city")
