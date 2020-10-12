from Project_Final_Scripts.Locations.locations import LocationFinder, Methods
from Project_Final_Scripts.Language.language_utils import LanguageUtil
from Project_Final_Scripts.date_utils import change_format, date2str, now
from Scrapping.chrome import ChromeManager
from Twitter import TwitterScrapper
import pandas as pd
import time
import re

csv_file = 'geo_tweets.csv'
count = 0
total = 0
LF = LocationFinder()
LU = LanguageUtil()
TS = TwitterScrapper(headless=True)
users = {}


def check_profile_location(row):
    # get user details
    place = TS.get_user_details(row.username)['place']

    # clean place text
    place = re.sub(r'\W', ' ', place)
    place = re.sub(r'\s{2,}', ' ', place)

    # check if the geo location of the tweets marches the user public location
    locations = LF.search_text(place, method={'en': Methods.SOUND, 'ar': Methods.EDIT_DISTANCE}, accepted_ratio=90)
    for location, ratio in locations:
        details = LF.get_location_details(location)
        if details['name'] == row.location:
            return details['name'], details
    return None, [l for (l, r) in locations]


def check_predicted_location(row):
    # get user tweets
    TS.load_page(f'https://twitter.com/{row.username}')
    TS.get_some_tweets(tweets_count=10)
    tweets = TS.get_tweets(as_dict=True)

    # predict locations
    locations = set()
    for key, tweet in tweets.items():
        if tweet['text']:
            predicted_locations = LF.search_text(
                tweet['text'],
                method={'en': Methods.SOUND, 'ar': Methods.EDIT_DISTANCE},
                accepted_ratio=90
            )
            for location, ratio in predicted_locations:
                locations.add(location)

    # check if any predicted location matched the geo location
    for location in locations:
        details = LF.get_location_details(location)
        if details['name'] == row.location:
            return details['name'], details
    return None, list(locations)


def get_location_data(row):
    global users

    # check if user already exists
    if row.username in users:
        return users[row.username]

    # match location to profile location
    user_l, user_d = check_profile_location(row)
    if user_l:
        users[row.username] = (user_l, user_d)
        return users[row.username]

    # match location to predicted locations
    p_l, p_d = check_predicted_location(row)
    if p_l:
        users[row.username] = (p_l, p_d)
        return users[row.username]

    # prefer current user profile over tweet geo location
    if len(user_d) > 0:
        users[row.username] = (user_d['name'], user_d)
        print(f'chosen profile location for {row.username}')
        return users[row.username]

    # prefer geo location over predicted location
    else:
        users[row.username] = (row.location, LF.get_location_details(row.location))
        print(f'chosen geo location for {row.username}')
        return users[row.username]


def get_data(row):
    global count

    time.sleep(0.5)

    location, location_details = get_location_data(row)

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
        # 'translated_text',
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

    df.to_csv('geo_tweets_extra.csv', index=False)


"""
#######################################################################################
"""


class Translate:

    def __init__(self):
        self._cm = ChromeManager()
        self._cm.load_page('https://translate.google.com/', '#source')

    def translate(self, text):
        self._cm.set_text('#source', text)
        time.sleep(3)
        return self._cm.get_text('span.tlid-translation.translation')

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
        return date2str(now())
    return change_format(date, from_format="%b %d", to_format='2020-%m-%d')


def fix_dates():
    df = pd.read_csv(csv_file, header=0)
    df.date = df.date.apply(fix_date)
    df.to_csv(csv_file, index=False)


if __name__ == '__main__':
    get_extra_data()
    # handle_null_data()
    # fix_dates()
