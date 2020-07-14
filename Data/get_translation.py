# import sys
# sys.path.insert(1, 'C:\\Users\\mohmad\\Desktop\\twitter')
from Data.handle_data import read_data, save_json
from twitter_config import CHROME_DRIVER
from Scrapping import ChromeManager
import time
import re


class Translate:

    def __init__(self, chrome_manager):
        self._cm: ChromeManager = chrome_manager
        self._cm.load_page('https://translate.google.com/', '#source')

    def translate(self, text):
        self._cm.set_value('#source', text)
        time.sleep(3)
        return self._cm.get_value('span.tlid-translation.translation')


def translate_specific_range(filename, t):
    range = input('Enter Range: (ex: 1-100)\n--> ').split('-')
    start = int(range[0])
    end = int(range[1])

    data = read_data(filename)
    data = data[start:end]

    res = []
    print(f'total count = {len(data)}')
    count = 0

    for d in data:
        if not d['username']:
            continue

        try:
            translated_text = t.translate(d['text'])
        except:
            print(f'Error in tweet {count}')
            translated_text = None

        res.append({
            'username': d['username'],
            'user-link': d['user-link'],
            'time': d['time'],
            'text': d['text'],
            'translated_text': translated_text,
            'tags': d['tags'],
            'location': None
        })

        count += 1
        if count % 10 == 0:
            print(count)

    saved_filename = filename.replace('without_html', 'translated')
    saved_filename = saved_filename.replace(".json", f'_range_{start}_{end}.json')
    save_json(saved_filename, res)


def translate_arabic_only(filename, t):
    arabic_regex = '[\u0621-\u064A]+'
    data = read_data(filename)
    res = []
    count = 0

    for d in data:
        if re.search(arabic_regex, d['text']):
            try:
                translated_text = t.translate(d['text'])
            except:
                continue
            count += 1
        else:
            translated_text = d['text']
        res.append({
            'username': d['username'],
            'user-link': d['user-link'],
            'time': d['time'],
            'text': d['text'],
            'translated_text': translated_text,
            'tags': d['tags'],
            'location': None
        })

    saved_filename = filename.replace('without_html', 'translated')
    save_json(saved_filename, res)
    print(count)


if __name__ == '__main__':
    cm = ChromeManager(driver_path=CHROME_DRIVER)
    t = Translate(cm)

    # translate_specific_range('sentimental_analysis\\without_html\\#corona_lebanon_tweets_11_7_2020.json', t)

    translate_arabic_only('sentimental_analysis\\without_html\\healthcare_tweets_10_7_2020.json', t)

    cm.close()
