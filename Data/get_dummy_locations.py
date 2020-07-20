from Locations.locations import LocationParser
from twitter_config import CITIES_JSON, CITIES_DETAILS_JSON
import re
from Data.handle_data import read_data, save_json


def get_arabic_aliases(location):
    aliases = LocationParser.get_location_aliases(location)
    arabic_aliases = []
    for alias in aliases:
        if re.search('[\u0621-\u064A]+', alias):
            arabic_aliases.append(alias)
    return arabic_aliases


def add_location_details(filename):
    data = read_data(filename)
    res = []
    for d in data:
        locations = LocationParser.get_locations(d['text'], similarity_ratio=0.75)
        location = None
        if locations:
            arabic_alises = get_arabic_aliases(locations[0][0])
            if arabic_alises:
                location = arabic_alises[0]
        if location:
            d['location'] = location
            l = LocationParser.Cities_Details[location]
            d['lat_long'] = f'{l["latitude"]},{l["longitude"]}'
        else:
            d['location'] = 'بيروت'
            d['lat_long'] = '33.8719,35.5097'
        res.append(d)

    parts = filename.split('\\')
    parts[1] = 'dummy_locations'
    new_name = "\\".join(parts)
    save_json(new_name, res)


def get_file_locations_frequencies(filename):
    data = read_data(filename)
    locations = {}
    for d in data:
        if d['location'] not in locations:
            locations[d['location']] = 1
        else:
            locations[d['location']] += 1
    sorted_locations = sorted(locations.items(), key=lambda l: l[1], reverse=True)

    for location in sorted_locations:
        print(location)


if __name__ == '__main__':
    LocationParser.load_locations(CITIES_JSON)
    LocationParser.load_locations_details(CITIES_DETAILS_JSON)
    print('[INFO]: Data Loaded!')

    files = [
        'sentimental_analysis\\sentimental_analysis\\#corona_lebanon_tweets_11_7_2020.json',
        'sentimental_analysis\\sentimental_analysis\\#corona_tweets_12_7_2020.json',
        'sentimental_analysis\\sentimental_analysis\\healthcare_tweets_10_7_2020.json',
        'sentimental_analysis\\sentimental_analysis\\medical_tweets_11_7_2020.json',
    ]

    for file in files:
        add_location_details(file)
        print(f'[COMPLETED] ==> {file}')
