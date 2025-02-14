from typing import List, Optional, Dict, Any

from geoalchemy2.shape import from_shape
from pydantic import BaseModel, Field
from shapely.geometry import shape
from sqlalchemy import func
from sqlalchemy.orm import Session

from database.schemas.DistrictSchema import DistrictSchema


class DistrictCreate(BaseModel):
    """
    Pydantic model for validating district creation data.
    """
    name: str = Field(..., min_length=1, max_length=200)  # District name, required, 1-200 characters
    boundaries: Dict[str, Any] = Field(..., description="Geographic boundaries in GeoJSON format")  # GeoJSON format
    city_id: int = Field(..., gt=0,
                         description="ID of the city associated with the district")  # City ID, must be greater than 0


def get_table_schema():
    return {column.name: column for column in DistrictSchema.__table__.columns}


def get_table_cols_with_geojson():
    cols = get_table_schema()
    cols["boundaries"] = func.ST_AsGeoJSON(DistrictSchema.boundaries).label("boundaries")
    return cols.values()


class DistrictResource:
    def __init__(self, db: Session):
        """
        Initialize the DistrictResource with a database session.

        :param db: SQLAlchemy database session.
        """
        self.db = db
        self.schema_geojson_cols = get_table_cols_with_geojson()  # A list with SQLAlchemy column objects that store geometry data in GeoJSON format.

    def get_all_districts(self) -> List[DistrictSchema]:
        """
        Retrieve all districts from the database.

        :return: A list of DistrictSchema instances representing all districts.
        """
        return self.db.query(*self.schema_geojson_cols).all()

    def get_district_by_id(self, district_id: int) -> Optional[DistrictSchema]:
        """
        Retrieve a single district by its ID.

        :param district_id: The ID of the district to retrieve.
        :return: A DistrictSchema instance representing the district, or None if no district is found.
        """
        return self.db.query(*self.schema_geojson_cols).filter(DistrictSchema.id == district_id).first()

    def get_districts_by_city(self, city_id: int) -> List[DistrictSchema]:
        """
        Retrieve all districts in a specific city.

        :param city_id: The ID of the city to filter districts by.
        :return: A list of DistrictSchema instances representing districts in the specified city.
        """
        return self.db.query(*self.schema_geojson_cols).filter(DistrictSchema.city_id == city_id).all()

    def create_district(self, district_data: DistrictCreate) -> DistrictSchema:
        """
        Create a new district in the database using validated data.

        :param district_data: A DistrictCreate instance containing the data for the new district.
        :return: A DistrictSchema instance representing the newly created district.
        """
        boundaries_geometry = from_shape(shape(district_data.boundaries), srid=4326)  # convert GeoJSON to WKT

        district = DistrictSchema(
            name=district_data.name,
            boundaries=boundaries_geometry,
            city_id=district_data.city_id
        )
        self.db.add(district)
        self.db.commit()
        self.db.refresh(district)
        return district

    def update_district(self, district_id: int, name: Optional[str] = None,
                        boundaries: Optional[Dict[str, Any]] = None) -> Optional[DistrictSchema]:
        """
        Update an existing district in the database.

        :param district_id: The ID of the district to update.
        :param name: The new name of the district (optional).
        :param boundaries: The new geographic boundaries of the district (in WKT format, optional).
        :return: The updated DistrictSchema instance, or None if no district is found.
        """
        district = self.db.query(DistrictSchema).filter(DistrictSchema.id == district_id).first()
        if district:
            if name:
                district.name = name
            if boundaries:
                district.boundaries = from_shape(shape(boundaries), srid=4326)  # GeoJSON -> GEOMETRY

            self.db.commit()
            self.db.refresh(district)
        return district

    def delete_district(self, district_id: int) -> bool:
        """
        Delete a district from the database.

        :param district_id: The ID of the district to delete.
        :return: True if the district was deleted, False otherwise.
        """
        district = self.db.query(DistrictSchema).filter(DistrictSchema.id == district_id).first()
        if district:
            self.db.delete(district)
            self.db.commit()
            return True
        return False
