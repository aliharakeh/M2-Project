from Twitter import TwitterScrapper
from urllib.parse import quote
import time
import json
import pandas as pd


def generate_url(keywords, lat, long, radius=3, since='2020-10-10'):
    keywords = quote(" OR ".join(keywords))
    return f'https://twitter.com/search?q=({keywords})%20geocode%3A{lat}%2C{long}%2C{radius}km%20since%3A{since}&src=typed_query&f=live'


def get_cities():
    with open('..\\..\\Locations\\cities_details.json', encoding='utf-8') as f:
        cities = json.loads(f.read())
    data = set()
    for key, city in cities.items():
        data.add((city['latitude'], city['longitude'], city['name']))
    return list(data)


if __name__ == '__main__':
    tw = TwitterScrapper(headless=True)
    data = {}
    cities = get_cities()
    keywords = [
        'corona',
        'covid',
        'كورونا',
        'كورونا_لبنان',
        'healthcare',
        'medical'
    ]

    for city in cities[:10]:
        lat, long, name = city
        url = generate_url(keywords, lat, long, radius=10)
        print(url)
        tw.load_page(url, max_tries=1, timeout=3)

        time.sleep(0.5)
        try:
            tw.get_all_tweets()
            data[tuple(city)] = tw.get_tweets()
            print(f'{name} DONE!!')
            print('---------------------------------------------')

        except Exception as e:
            print(e)
            print(f'[Error] => saved {len(tw.tweets)} tweets')

    final_data = []
    for key, tweets in data.items():
        for details in tweets:
            final_data.append([*details, *key])

    print(final_data)
    df = pd.DataFrame(final_data, columns=['username', 'time', 'text', 'tags', 'latitude', 'longitude', 'location'])
    df.to_csv('geo_tweets2.csv', index=False)
