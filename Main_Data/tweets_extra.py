from Locations.locations import LocationParser
from textblob import TextBlob
import pandas as pd


def get_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity


def get_label(sentiment):
    if sentiment == 0:
        return 'Neutral'
    return 'Positive' if sentiment > 0 else 'Negative'


count = 0


def get_location_data(text):
    global count

    try:
        loc = LocationParser.get_locations(text)
        if loc:
            arabic_aliases = LocationParser.get_arabic_alias(loc[0][0])
            if arabic_aliases:
                location = arabic_aliases
            else:
                location = loc[0][0]

            location_details = LocationParser.Cities_Details[location]

        else:
            location = 'بيروت'
            location_details = LocationParser.Cities_Details[location]

        count += 1
        print(count)
        return pd.Series([
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
        return pd.Series([None, None, None, None, None, None, None, None, None])


if __name__ == '__main__':
    LocationParser.load_locations()
    LocationParser.load_locations_details()

    df = pd.read_csv('tweets_sentiment.csv', header=0)

    # df['sentiment'] = df['translated_text'].apply(get_sentiment)
    # df['sentiment_label'] = df['sentiment'].apply(get_label)

    df[[
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

    df.to_csv('tweets_v2.csv', index=False)
