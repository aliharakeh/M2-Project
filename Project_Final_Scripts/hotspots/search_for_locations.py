from google_maps.google_maps import search_google_maps, split_clean_text
import json
import os
import time

DIR = os.path.dirname(__file__)

stopwords = ['http', 'https', 'com']
with open(f'{DIR}\\..\\..\\stop-words\\english.txt', encoding='utf-8') as f:
    stopwords += f.read().split('\n')


def search_text(text):
    # split text into words
    words = split_clean_text(text)

    # check if any word refers to a location
    # places = []
    for word in words:
        if word.strip().lower() in stopwords:
            continue
        try:
            place = search_google_maps(word, proxy=False)
            if place and place[0] != "64653.2798905912":
                # print(f'[Location]: {word}')
                # places.append({
                #     'word': word,
                #     'context': text,
                #     'place': place
                # })
                return True
        except:
            # print(f'[Error Word]: `{word}`')
            pass
        time.sleep(1)

    return False


if __name__ == '__main__':
    with open('hotspots_cleaned_v2.json', encoding='utf-8') as f:
        hotspots = json.loads(f.read())

    data = {}
    days = list(hotspots.keys())
    start = 0
    end = len(days)

    # iterate hotspots
    for day in days[start: end]:
        print(f'[Date]: {day}')

        details = hotspots[day]
        data[day] = {}

        # iterate trends
        for trend in details['trends']:
            topic, link, tweets = trend['topic'], trend['link'], trend['tweets']
            print(f'[Trend]: {topic} - [Link]: {link}')

            data[day][topic] = []

            # iterate tweets
            for i, tweet in enumerate(tweets):
                print(f'Processing Tweet {i} of `{topic}`...')
                if search_text(tweet):
                    data[day][topic].append(tweet)

            print(f'[Tweets]: {len(tweets)} - [Location Tweets]: {len(data[day][topic])}')
            print('---------------------------------------------------------------')

        # separate dates
        print('################################################################################')

    with open(f'hotspots_locations_days_{start}_{end}.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, indent=2, ensure_ascii=False))
