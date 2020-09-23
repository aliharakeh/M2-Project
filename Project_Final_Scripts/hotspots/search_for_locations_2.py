import json
import time
import re
from Scrapping import ChromeManager

# use chrome driver to open google maps
cm = ChromeManager(verbose=False)
cm.load_page('https://www.google.com/maps')


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


def search_google_maps(word):
    # automate the input in the search field the location name and run the search
    cm.set_value('input#searchboxinput', word)

    cm.click_element('#searchbox-searchbutton', delay_after_click=2)

    return None


if __name__ == '__main__':
    with open('hotspots.json', encoding='utf-8') as f:
        hotspots = json.loads(f.read())

    hotspots_locations = {}
    choice = None

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
                    # try getting the location
                    try:
                        place = search_google_maps(word)
                        if place:
                            hotspots_locations[date][trend].append(place)

                    # if not, then fix issue then retry
                    except:
                        choice = input('Fix any issue then press [y] to continue or anything else to stop')
                        if choice != 'y':
                            break

                    # sleep
                    time.sleep(1)

                if choice != 'y':
                    break

            if choice != 'y':
                break

        if choice != 'y':
            break

    cm.close()

    with open('hotspots_locations.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(hotspots_locations, indent=2, ensure_ascii=False))
