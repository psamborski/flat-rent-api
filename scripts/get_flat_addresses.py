import json
import traceback

from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="coordinateconverter")
flats = []


def get_flat_data_with_address(flat_data):
    try:
        print(f'\nScrapping for flat offer: {flat_data["title"]}...')
        location = geolocator.reverse(f"{flat_data['latitude']}, {flat_data['longitude']}")

        full_flat_data = {
            **m,
            "address": f"{location.raw['address'].get('road', '')} M/N",
            "house_number": location.raw['address'].get("house_number", ""),
            # "flat_number": 0,
            "quarter": location.raw['address'].get("quarter", ""),
            "suburb": location.raw['address'].get("suburb", ""),
            "state": location.raw['address'].get("state", "")
        }

        print('OK')
    except Exception as e:
        print(traceback.format_exc())
        full_flat_data = {
            **m,
            "address": "",
            "house_number": "",
            # "flat_number": 0,
            "quarter": "",
            "suburb": "",
            "state": "",
        }
    return full_flat_data


if __name__ == "__main__":
    with open('../static_data/flat_rent_api.json') as f:
        db = json.load(f)

        print('Getting addresses for flats...')
        for m in db["flats"]:
            flat_full_data = get_flat_data_with_address(m)
            flats.append(flat_full_data)

        # if errors occurred, try to get all flats' data until some number of tries
        print('Checking for errors in addresses...')
        all_good = False
        retries = 1

        while all_good is False and retries <= 5:
            print(f'\nRetry #{retries}')
            not_scrapped_addresses_num = 0
            for m in flats:
                if m["address"] == "":
                    print(f'\nNo address in flat title: {m["title"]}')
                    flat_full_data = get_flat_data_with_address(m)
                    flats[flats.index(m)] = flat_full_data
                    not_scrapped_addresses_num += 1

            all_good = not_scrapped_addresses_num == 0
            retries += 1

        if all_good:
            print('Everything OK!')
        else:
            print(f'Failed to get addresses for {not_scrapped_addresses_num} flats!')
        db["flats"] = flats

    with open('../static_data/flat_rent_api-addresses.json', 'w', encoding='utf-8') as f:
        print('\nSaving data to /static_data/flat_rent_api-addresses.json...')
        json.dump(db, f, ensure_ascii=False, indent=4)
        print('Done!')
