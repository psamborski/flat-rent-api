from typing import List, Optional
from sqlalchemy.orm import Session

from database.schemas.AmenitySchema import AmenitySchema


class AmenityResource:
    def __init__(self, db: Session):
        """
        Initialize the AmenityResource with a database session.

        :param db: SQLAlchemy database session.
        """
        self.db = db

    def get_all_amenities(self) -> List[AmenitySchema]:
        """
        Retrieve all amenities from the database.

        :return: A list of AmenitySchema instances representing all amenities.
        """
        return self.db.query(AmenitySchema).all()

    def get_amenity_by_id(self, amenity_id: int) -> Optional[AmenitySchema]:
        """
        Retrieve a single amenity by its ID.

        :param amenity_id: The ID of the amenity to retrieve.
        :return: An AmenitySchema instance representing the amenity, or None if no amenity is found.
        """
        return self.db.query(AmenitySchema).filter(AmenitySchema.id == amenity_id).first()

    def get_amenity_by_name(self, name: str) -> Optional[AmenitySchema]:
        """
        Retrieve a single amenity by its name.

        :param name: The name of the amenity to retrieve.
        :return: An AmenitySchema instance representing the amenity, or None if no amenity is found.
        """
        return self.db.query(AmenitySchema).filter(AmenitySchema.name == name).first()

    def create_amenity(self, name: str) -> AmenitySchema:
        """
        Create a new amenity in the database.

        :param name: The name of the new amenity.
        :return: An AmenitySchema instance representing the newly created amenity.
        """
        amenity = AmenitySchema(name=name)
        self.db.add(amenity)
        self.db.commit()
        self.db.refresh(amenity)
        return amenity

    def delete_amenity(self, amenity_id: int) -> bool:
        """
        Delete an amenity from the database.

        :param amenity_id: The ID of the amenity to delete.
        :return: True if the amenity was deleted, False otherwise.
        """
        amenity = self.db.query(AmenitySchema).filter(AmenitySchema.id == amenity_id).first()
        if amenity:
            self.db.delete(amenity)
            self.db.commit()
            return True
        return False