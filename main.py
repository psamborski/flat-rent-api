from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database.database import SessionLocal

# Import schemas and models
from models import City, Amenity, Flat, CityCreate, AmenityCreate, FlatCreate
from database.schemas import CitySchema, AmenitySchema, FlatSchema, FlatAmenitySchema

# FastAPI app initialization
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Dummy flat rent API."}


    finally:
        db.close()


# Create a new city
@app.post("/cities/", response_model=City)
def create_city(city: CityCreate, db: Session = Depends(get_db)):
    db_city = CitySchema(name=city.name, country=city.country)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


# Create a new amenity
@app.post("/amenities/", response_model=Amenity)
def create_amenity(amenity: AmenityCreate, db: Session = Depends(get_db)):
    db_amenity = AmenitySchema(name=amenity.name)
    db.add(db_amenity)
    db.commit()
    db.refresh(db_amenity)
    return db_amenity


# Create a new flat
@app.post("/flats/", response_model=Flat)
def create_flat(flat: FlatCreate, db: Session = Depends(get_db)):
    db_flat = FlatSchema(
        title=flat.title,
        description=flat.description,
        address=flat.address,
        latitude=flat.latitude,
        longitude=flat.longitude,
        floor=flat.floor,
        rooms_number=flat.rooms_number,
        square=flat.square,
        price=flat.price,
        currency=flat.currency,
        city_id=flat.city_id
    )
    db.add(db_flat)
    db.commit()
    db.refresh(db_flat)

    # Add amenities to flat using FlatAmenity table
    for amenity_id in flat.amenities_ids:
        db_flat_amenity = FlatAmenitySchema(flat_id=db_flat.id, amenity_id=amenity_id)
        db.add(db_flat_amenity)

    db.commit()
    db.refresh(db_flat)

    return db_flat


# Get all flats
@app.get("/flats/", response_model=List[Flat])
def get_flats(db: Session = Depends(get_db)):
    return db.query(FlatSchema).all()


# Get a flat by id
@app.get("/flats/{flat_id}", response_model=Flat)
def get_flat(flat_id: int, db: Session = Depends(get_db)):
    db_flat = db.query(FlatSchema).filter(FlatSchema.id == flat_id).first()
    if db_flat is None:
        raise HTTPException(status_code=404, detail="Flat not found")
    return db_flat