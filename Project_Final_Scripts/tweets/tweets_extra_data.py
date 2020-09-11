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


def get_location_data(text):
    global count

    try:
        loc = LF.search_text(text, method={'en': Methods.SOUND, 'ar': Methods.EDIT_DISTANCE})
        if loc:
            arabic_aliases = LF.get_arabic_alias(loc[0][0])
            if arabic_aliases:
                location = arabic_aliases
            else:
                location = loc[0][0]
        else:
            location = 'بيروت'

        location_details = LF.get_location_details(location)

        translated_text = LU.quick_translation(text)

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

    except:
        return pd.Series([None, None, None, None, None, None, None, None, None, None])

    finally:
        count += 1
        print(count, '/', total)
        time.sleep(0.5)


if __name__ == '__main__':
    df = pd.read_csv(read_from, header=0)
    total = len(df)

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
    ]] = df['text'].apply(get_location_data)

    df.to_csv(save_to, index=False)
