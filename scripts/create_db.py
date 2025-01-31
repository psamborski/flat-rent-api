import json
import traceback

from sqlalchemy import text
from sqlalchemy.orm import Session
from database.database import engine, Base
from database.schemas import CitySchema, AmenitySchema, FlatSchema, FlatAmenitySchema

# Create schema if it doesn't exist
def create_schema():
    print("Creating DB schema...")

    with engine.connect() as connection:
        connection.execute(text("CREATE SCHEMA IF NOT EXISTS flat_rent_api;"))
        connection.commit()

# Create tables in DB
def create_tables():
    print("Creating DB tables...")

    Base.metadata.create_all(bind=engine)

# Load data from JSON file
def load_data_from_json(filename='static_data/flat_rent_api-addresses.json'):
    print(f"Loading data from {filename}...")

    with open(filename, "r") as file:
        data = json.load(file)

    with Session(engine) as session:
        for city_data in data["cities"]:
            city = CitySchema(**city_data)
            session.add(city)

        for amenity_data in data["amenities"]:
            amenity = AmenitySchema(**amenity_data)
            session.add(amenity)

        for flat_data in data["flats"]:
            flat = FlatSchema(**flat_data)
            session.add(flat)

        session.commit()

if __name__ == "__main__":
    try:
        # Create schema to distinct app table from built-in tables
        create_schema()

        # Create tables if they don't exist
        create_tables()

        print("DB schema and tables created successfully!")
    except Exception as e:
        print(f"DB creation failed.\n\nTraceback:")
        print(traceback.format_exc())
        print(f"\nError: {e}")

    try:
        # Load data from given JSON file
        # load_data_from_json()
        ...
    except Exception as e:
        print(f"Data loading failed.\n\nTraceback:")
        print(traceback.format_exc())
        print(f"\nError: {e}")