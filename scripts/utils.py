from geoalchemy2 import WKTElement


def reformat_flat_data(flat_data):
    return {
        "title": flat_data.get("title", ""),
        "description": flat_data.get("description", ""),
        "address": flat_data.get("address", ""),
        "coordinates": WKTElement(f"POINT({flat_data.get('longitude', '')} {flat_data.get('latitude', '')})",
                                  srid=4326),
        "floor": flat_data.get("floor", 0),
        "rooms_number": flat_data.get("rooms_number", 0),
        "square": flat_data.get("square", 0),
        "price": flat_data.get("price", 0),
        "currency": flat_data.get("currency", None),
        "city_id": flat_data.get("city_id", 1),
    }
