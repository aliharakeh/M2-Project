from Locations.locations_v2 import LocationFinder, Methods
from Language.language_utils import LanguageUtil
from Scrapping.chrome import ChromeManager
import pandas as pd
import time
from datetime import datetime

csv_file = 'tweets.csv'
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
        if loc and loc[0][0]:
            arabic_aliases = LF.get_arabic_alias(loc[0][0])
            if arabic_aliases:
                location = arabic_aliases
            else:
                location = loc[0][0]
        else:
            raise ValueError('Error')
    except:
        location = 'بيروت'

    finally:
        location_details = LF.get_location_details(location)
        users[username] = (location, location_details)

    return users[username]


def get_data(row):
    global count

    time.sleep(0.5)

    location, location_details = get_location_data(row.username, row.text)

    try:
        translated_text = LU.quick_translation(row.text)['translated']
    except:
        translated_text = None

    count += 1
    if count % 10 == 0:
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


def get_extra_data():
    global total

    df = pd.read_csv(csv_file, header=0)
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

    df.to_csv(csv_file, index=False)


"""
#######################################################################################
"""


class Translate:

    def __init__(self):
        self._cm = ChromeManager()
        self._cm.load_page('https://translate.google.com/', '#source')

    def translate(self, text):
        self._cm.set_value('#source', text)
        time.sleep(3)
        return self._cm.get_value('span.tlid-translation.translation')

    def close(self):
        self._cm.close()


T = None


def translate(text):
    try:
        return T.translate(text)
    except:
        print(text)
        return input('\n\nenter translation manually\n ==> ')


def handle_null_data():
    global T

    T = Translate()
    df = pd.read_csv(csv_file, header=0)

    null_text = df[df.text.isna()]
    print('Null Text:', len(null_text))
    null_translations = df[df.translated_text.isna()]
    print('Null Translations:', len(null_translations))

    print('Removing Null Text...')
    df.dropna(subset=['text'], inplace=True)
    print('Removed Null Text!!')

    print('Translating...')
    df.loc[df.translated_text.isna(), 'translated_text'] = null_translations.text.apply(translate)
    print('Translation Done!!')

    df.to_csv(csv_file, index=False)

    T.close()


"""
#######################################################################################
"""


def fix_date(date):
    if 'h' in date or 'm' in date or 's' in date:
        return '2020-10-01'
    return datetime.strptime(date, "%b %d").strftime('2020-%m-%d')


def fix_dates():
    df = pd.read_csv(csv_file, header=0)
    df.date = df.date.apply(fix_date)
    df.to_csv(csv_file, index=False)


if __name__ == '__main__':
    get_extra_data()
    handle_null_data()
    fix_dates()
