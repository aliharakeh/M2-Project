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


def log(msg, error=False):
    if error:
        logging.error(msg)
    else:
        logging.info(msg)
    print(msg)


def camel_case_split(str):
    words = [[str[0]]]
    for c in str[1:]:
        if words[-1][-1].islower() and c.isupper():
            words.append(list(c))
        else:
            words[-1].append(c)
    return [''.join(word) for word in words]


def split_clean_text(text):
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


def search_text(topic, link, text):
    # split text into words
    words = split_clean_text(text)

    places = []

    # check if any word refers to a location
    for word in words:
        try:
            place = search_google_maps(word)
            if place:
                log(f'[Word]: `{word}` - [Trend]: {topic} - [Link]: {link} - [Location]: {place}')
                places.append(place)
        except:
            log(f'[Error Word]: `{word}` - [Trend]: {topic} - [Link]: {link}', error=True)

    return places


if __name__ == '__main__':
    with open('hotspots.json', encoding='utf-8') as f:
        hotspots = json.loads(f.read())

    hotspots_locations = {}

    # iterate hotspots
    for date, hotspot in hotspots.items():
        hotspots_locations[date] = {}

        log(f'[Date]: {date}')

        # iterate trends
        for trend in hotspot['trends']:
            hotspots_locations[date][trend['topic']] = []
            log(f'[Trend]: {trend["topic"]}')

            # iterate tweets
            for i, tweet in enumerate(trend['tweets']):

                log(f'Processing Tweet {i}...')

                # split text into words
                words = split_clean_text(tweet)

                # check if any word refers to a location
                for word in words:
                    print(word)
                    try:
                        place = search_google_maps(word)
                        if place:
                            hotspots_locations[date][trend].append(place)
                            log(f'[Word]: `{word}` - [Trend]: {trend["topic"]} - [Link]: {trend["link"]} - [Location]: {place}')
                    except:
                        log(f'[Error Word]: `{word}` - [Trend]: {trend["topic"]} - [Link]: {trend["link"]}', error=True)
                    time.sleep(0.5)

            log(f'[Trend]: {trend["topic"]} - {len(trend["tweets"])} tweets - {len(hotspots_locations[date][trend])} location(s) found')

        log('---------------------------------------------')

    with open('hotspots_locations.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(hotspots_locations, indent=2, ensure_ascii=False))
