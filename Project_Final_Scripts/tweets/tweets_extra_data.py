from Locations.locations_v2 import LocationFinder, Methods
from Language.language_utils import LanguageUtil
import pandas as pd
import time

read_from = 'tweets.csv'
save_to = 'tweets_v2.csv'
count = 0
total = 0
LF = LocationFinder()
LU = LanguageUtil()
users = {}


def get_location_data(username, text):
    global users

    if username in users:
        return users[username]

    location = None
    try:
        loc = LF.search_text(text, method={'en': Methods.SOUND, 'ar': Methods.EDIT_DISTANCE})
        if loc:
            arabic_aliases = LF.get_arabic_alias(loc[0][0])
            if arabic_aliases:
                location = arabic_aliases
            else:
                location = loc[0][0]
    except:
        location = 'بيروت'

    finally:
        location_details = LF.get_location_details(location)
        users[username] = (location, location_details)

    return users[username]


def get_data(row):
    global count

    location, location_details = get_location_data(row.username, row.text)

    try:
        translated_text = LU.quick_translation(row.text)['translated']
    except:
        translated_text = None

    count += 1
    if count % 20 == 0:
        print(count, '/', total)

    return pd.Series([
        translated_text,
        location,
        location_details['latitude'],
        location_details['longitude'],
        location_details['KADAA_ID'],
        location_details['KADAA_AR'],
        location_details['KADAA_EN'],
        location_details['MOHAFAZA_ID'],
        location_details['MOHAFAZA_AR'],
        location_details['MOHAFAZA_EN']
    ])


if __name__ == '__main__':
    df = pd.read_csv(read_from, header=0)
    total = len(df)

    df.username.fillna('UserX', inplace=True)

    df[[
        'translated_text',
        'location',
        'latitude',
        'longitude',
        'KADAA_ID',
        'KADAA_AR',
        'KADAA_EN',
        'MOHAFAZA_ID',
        'MOHAFAZA_AR',
        'MOHAFAZA_EN'
    ]] = df.apply(get_data, axis=1)

    df.to_csv(save_to, index=False)

