from database.schemas.AmenitySchema import AmenitySchema
from database.schemas.CitySchema import CitySchema
from database.schemas.FlatAmenitySchema import FlatAmenitySchema
from database.schemas.FlatSchema import FlatSchema
from helpers.scripts.utils import reformat_flat_data

def add_cities(session, cities_data):
    cities = [CitySchema(**city_data) for city_data in cities_data]
    session.add_all(cities)
    session.commit()
    return cities


def add_amenities(session, amenities_data):
    amenities = [AmenitySchema(**amenity_data) for amenity_data in amenities_data]
    session.add_all(amenities)
    session.commit()
    return amenities


def add_flats(session, flats_data):
    flats = []
    for flat_data in flats_data:
        flat_data_reformatted = reformat_flat_data(flat_data)
        flat = FlatSchema(**flat_data_reformatted)
        flats.append(flat)
        session.add(flat)
    session.commit()
    return flats


def add_flat_amenities(session, flats_json_data, flats_db_data):
    flat_amenities = []
    for flat_json, flat_db in zip(flats_json_data, flats_db_data):
        for amenity_id in flat_json["amenities"]:
            flat_amenities.append(FlatAmenitySchema(flat_id=flat_db.id, amenity_id=amenity_id))
    session.add_all(flat_amenities)
    session.commit()
    return flat_amenities
