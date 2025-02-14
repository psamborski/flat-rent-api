from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import and_

from database.FlatAmenitySchema import FlatAmenitySchema


class FlatAmenityResource:
    def __init__(self, db: Session):
        """
        Initialize the FlatAmenityResource with a database session.

        :param db: SQLAlchemy database session.
        """
        self.db = db

    def get_all_flat_amenities(self) -> List[FlatAmenitySchema]:
        """
        Retrieve all flat-amenity relationships from the database.

        :return: A list of FlatAmenitySchema instances representing all flat-amenity relationships.
        """
        return self.db.query(FlatAmenitySchema).all()

    def get_amenities_by_flat(self, flat_id: int) -> List[FlatAmenitySchema]:
        """
        Retrieve all amenities associated with a specific flat.

        :param flat_id: The ID of the flat to retrieve amenities for.
        :return: A list of FlatAmenitySchema instances representing the amenities for the specified flat.
        """
        return self.db.query(FlatAmenitySchema).filter(FlatAmenitySchema.flat_id == flat_id).all()

    def get_flats_by_amenity(self, amenity_id: int) -> List[FlatAmenitySchema]:
        """
        Retrieve all flats associated with a specific amenity.

        :param amenity_id: The ID of the amenity to retrieve flats for.
        :return: A list of FlatAmenitySchema instances representing the flats for the specified amenity.
        """
        return self.db.query(FlatAmenitySchema).filter(FlatAmenitySchema.amenity_id == amenity_id).all()

    def create_flat_amenity(self, flat_id: int, amenity_id: int) -> FlatAmenitySchema:
        """
        Create a new flat-amenity relationship in the database.

        :param flat_id: The ID of the flat.
        :param amenity_id: The ID of the amenity.
        :return: A FlatAmenitySchema instance representing the newly created relationship.
        """
        flat_amenity = FlatAmenitySchema(flat_id=flat_id, amenity_id=amenity_id)
        self.db.add(flat_amenity)
        self.db.commit()
        self.db.refresh(flat_amenity)
        return flat_amenity

    def delete_flat_amenity(self, flat_id: int, amenity_id: int) -> bool:
        """
        Delete a flat-amenity relationship from the database.

        :param flat_id: The ID of the flat.
        :param amenity_id: The ID of the amenity.
        :return: True if the relationship was deleted, False otherwise.
        """
        flat_amenity = self.db.query(FlatAmenitySchema).filter(
            and_(FlatAmenitySchema.flat_id == flat_id, FlatAmenitySchema.amenity_id == amenity_id)
        ).first()
        if flat_amenity:
            self.db.delete(flat_amenity)
            self.db.commit()
            return True
        return False