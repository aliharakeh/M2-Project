from google_maps.google_maps import search_google_maps
import json
import time
import re
import logging

logging.basicConfig(
    format='%(levelname)s:%(message)s',
    filename='search_for_locations.log',
    level=logging.ERROR,
    filemode='w'
)


def camel_case_split(str):
    words = [[str[0]]]
    for c in str[1:]:
        if words[-1][-1].islower() and c.isupper():
            words.append(list(c))
        else:
            words[-1].append(c)
    return [''.join(word) for word in words]


def clean(text):
    text = str(text)
    text = re.sub(r'\n|\W|_', ' ', text)
    words = [w.strip() for w in text.split() if len(w) > 2]
    res = []
    for word in words:
        data = camel_case_split(word)
        for d in data:
            if len(d) > 2:
                res.append(d.lower())
    return res


if __name__ == '__main__':
    with open('hotspots.json', encoding='utf-8') as f:
        hotspots = json.loads(f.read())

    hotspots_locations = {}

    # iterate hotspots
    for date, hotspot in hotspots.items():
        hotspots_locations[date] = {}

        # iterate trends
        for trend in hotspot['trends']:
            hotspots_locations[date][trend['topic']] = []

            # iterate tweets
            for tweet in trend['tweets']:
                # split text into words
                words = clean(tweet)

                # check if any word refers to a location
                for word in words:
                    try:
                        place = search_google_maps(word)
                        if place:
                            hotspots_locations[date][trend].append(place)
                    except:
                        logging.error(f'[Word]: `{word}` - [Trend]: {trend["topic"]} - [Link]: {trend["link"]}')
                    time.sleep(1)
                break
            break
        break

    with open('hotspots_locations.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(hotspots_locations, indent=2, ensure_ascii=False))
