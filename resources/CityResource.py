from typing import List, Optional, Dict, Any

from geoalchemy2.shape import from_shape
from pydantic import BaseModel, Field
from sqlalchemy import func
from sqlalchemy.orm import Session
from shapely.geometry import shape


from database.schemas.CitySchema import CitySchema


class CityCreate(BaseModel):
    """
    Pydantic model for validating city creation data.
    """
    name: str = Field(..., min_length=1, max_length=200)  # City name, required, 1-200 characters
    boundaries: Dict[str, Any] = Field(..., description="Geographic boundaries in GeoJSON format")  # GeoJSON format
    country: str = Field(..., max_length=200)  # Country name, required, 1-200 characters


def get_table_schema():
    return {column.name: column for column in CitySchema.__table__.columns}

def get_table_cols_with_geojson():
    cols = get_table_schema()
    cols["boundaries"] = func.ST_AsGeoJSON(CitySchema.boundaries).label("boundaries")
    return cols.values()


class CityResource:
    def __init__(self, db: Session):
        """
        Initialize the CityResource with a database session.

        :param db: SQLAlchemy database session.
        """
        self.db = db
        self.schema_geojson_cols = get_table_cols_with_geojson()  # A list with SQLAlchemy column objects that store geometry data in GeoJSON format.

    def get_all_cities(self) -> List[CitySchema]:
        """
        Retrieve all cities from the database.

        :return: A list of CitySchema instances representing all cities.
        """
        return self.db.query(*self.schema_geojson_cols).all()

    def get_city_by_id(self, city_id: int) -> Optional[CitySchema]:
        """
        Retrieve a single city by its ID.

        :param city_id: The ID of the city to retrieve.
        :return: A CitySchema instance representing the city, or None if no city is found.
        """
        return self.db.query(*self.schema_geojson_cols).filter(CitySchema.id == city_id).first()

    def get_cities_by_country_name(self, country_name: str) -> List[CitySchema]:
        """
        Retrieve all cities by country name.

        :param country_name: The name of the country to filter cities by.
        :return: A list of CitySchema instances representing cities in the specified city.
        """
        return self.db.query(*self.schema_geojson_cols).filter(CitySchema.country == country_name).all()

    def create_city(self, city_data: CityCreate) -> CitySchema:
        """
        Create a new city in the database using validated data.

        :param city_data: A CityCreate instance containing the data for the new city.
        :return: A CitySchema instance representing the newly created city.
        """
        boundaries_geometry = from_shape(shape(city_data.boundaries), srid=4326)  # convert GeoJSON to WKT

        city = CitySchema(
            name=city_data.name,
            boundaries=boundaries_geometry,
            country=city_data.country
        )
        self.db.add(city)
        self.db.commit()
        self.db.refresh(city)
        return city

    def update_city(self, city_id: int, name: Optional[str] = None, boundaries: Optional[Dict[str, Any]] = None, country: Optional[str] = None) -> Optional[CitySchema]:
        """
        Update an existing city in the database.

        :param city_id: The ID of the city to update.
        :param name: The new name of the city (optional).
        :param boundaries: The new geographic boundaries of the city (in WKT format, optional).
        :param country: The new name of the city's country (optional).
        :return: The updated CitySchema instance, or None if no city is found.
        """
        city = self.db.query(CitySchema).filter(CitySchema.id == city_id).first()
        if city:
            if name:
                city.name = name
            if boundaries:
                city.boundaries = from_shape(shape(boundaries), srid=4326)  # GeoJSON -> GEOMETRY
            if country:
                city.country = country

            self.db.commit()
            self.db.refresh(city)
        return city

    def delete_city(self, city_id: int) -> bool:
        """
        Delete a city from the database.

        :param city_id: The ID of the city to delete.
        :return: True if the city was deleted, False otherwise.
        """
        city = self.db.query(CitySchema).filter(CitySchema.id == city_id).first()
        if city:
            self.db.delete(city)
            self.db.commit()
            return True
        return False