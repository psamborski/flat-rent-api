from typing import List, Optional

from geoalchemy2.shape import from_shape
from shapely.geometry import shape
from sqlalchemy import func
from sqlalchemy.orm import Session

from api.schemas.FlatApiSchema import FlatCreate, FlatUpdate
from database.schemas.FlatSchema import FlatSchema


def get_table_schema():
    return {column.name: column for column in FlatSchema.__table__.columns}


def get_table_cols_with_geojson():
    cols = get_table_schema()
    cols["coordinates"] = func.ST_AsGeoJSON(FlatSchema.coordinates).label("coordinates")
    return cols.values()


class FlatResource:
    def __init__(self, db: Session):
        """
        Initialize the FlatResource with a database session.

        :param db: SQLAlchemy database session.
        """
        self.db = db
        self.schema_geojson_cols = get_table_cols_with_geojson()  # A list with SQLAlchemy column objects that store geometry data in GeoJSON format.

    def get_all_flats(self) -> List[FlatSchema]:
        """
        Retrieve all flats from the database.

        :return: A list of FlatSchema instances representing all flats in the database.
        """
        return self.db.query(*self.schema_geojson_cols).all()

    def get_flat_by_id(self, flat_id: int) -> Optional[FlatSchema]:
        """
        Retrieve a single flat by its ID.

        :param flat_id: The ID of the flat to retrieve.
        :return: A FlatSchema instance representing the flat, or None if no flat is found.
        """
        return self.db.query(*self.schema_geojson_cols).filter(FlatSchema.id == flat_id).first()

    def get_flats_by_district(self, district_id: int) -> List[FlatSchema]:
        """
        Retrieve all flats in a specific district.

        :param district_id: The ID of the district to filter flats by.
        :return: A list of FlatSchema instances representing flats in the specified district.
        """
        return self.db.query(*self.schema_geojson_cols).filter(FlatSchema.district_id == district_id).all()

    def get_flats_by_city(self, city_id: int) -> List[FlatSchema]:
        """
        Retrieve all flats in a specific city.

        :param city_id: The ID of the city to filter flats by.
        :return: A list of FlatSchema instances representing flats in the specified city.
        """
        return self.db.query(*self.schema_geojson_cols).filter(FlatSchema.city_id == city_id).all()

    def create_flat(self, flat_data: FlatCreate) -> FlatSchema:
        """
        Create a new flat in the database.

        :param flat_data: A FlatCreate instance containing the data for the new flat.
        :return: A FlatSchema instance representing the newly created flat.
        """
        point_geometry = from_shape(shape(flat_data.coordinates), srid=4326)  # convert GeoJSON to WKT

        flat = FlatSchema(
            title=flat_data.title,
            description=flat_data.description,
            address=flat_data.address,
            coordinates=point_geometry,  # in WKT format
            floor=flat_data.floor,
            rooms_number=flat_data.rooms_number,
            square=flat_data.square,
            price=flat_data.price,
            currency=flat_data.currency,
            city_id=flat_data.city_id,
            district_id=flat_data.district_id,
        )
        self.db.add(flat)
        self.db.commit()
        self.db.refresh(flat)
        return flat

    def update_flat(self, flat_data: FlatUpdate) -> FlatSchema:
        """
        Update an existing flat in the database.

        :param flat_data: A FlatUpdate instance containing the data for the new flat.
        :return: The updated FlatSchema instance.
        """
        flat = self.get_flat_by_id(flat_data.id)

        if flat:
            update_dict = flat_data.model_dump(exclude_unset=True, exclude={'id'})  # Pomija wartości None

            # Convert GeoJSON to WKT if needed
            if "coordinates" in update_dict and update_dict["coordinates"]:
                update_dict["coordinates"] = from_shape(shape(update_dict["coordinates"]), srid=4326)

            for key, value in update_dict.items():
                setattr(flat, key, value)  # Dynamiczne przypisywanie wartości

            self.db.commit()
            self.db.refresh(flat)
        return flat



    def delete_flat(self, flat_id: int) -> bool:
        """
        Delete a flat from the database.

        :param flat_id: The ID of the flat to delete.
        :return: True if the flat was deleted, False otherwise.
        """
        district = self.db.query(FlatSchema).filter(FlatSchema.id == flat_id).first()
        if district:
            self.db.delete(district)
            self.db.commit()
            return True
        return False
