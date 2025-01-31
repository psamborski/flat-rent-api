import json
import traceback

from sqlalchemy import text
from sqlalchemy.orm import Session

from database.database import engine, Base
from scripts.add_data_to_db import add_cities, add_amenities, add_flats, add_flat_amenities


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
def insert_data_from_json_to_db(filename='static_data/flat_rent_api-addresses.json'):
    print(f"Loading data from {filename}...")

    with open(filename, "r") as file:
        data = json.load(file)

    with Session(engine) as session:
        # Add cities
        add_cities(session, data["cities"])

        # Add amenities
        add_amenities(session, data["amenities"])

        # Add flats
        flats = add_flats(session, data["flats"])

        # Add associations between flats and amenities
        add_flat_amenities(session, data["flats"], flats)


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
        insert_data_from_json_to_db()
        print(
            "Data loaded successfully!\n"
            "You can now run the app and use the API.")
    except Exception as e:
        print(f"Data loading failed.\n\nTraceback:")
        print(traceback.format_exc())
        print(f"\nError: {e}")
