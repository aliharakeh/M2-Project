from Scrapping import ChromeManager
from twitter_config import CHROME_DRIVER
from Data.handle_data import read_data, save_json
import time


class Translate:

    def __init__(self, chrome_manager):
        self._cm: ChromeManager = chrome_manager
        self._cm.load_page('https://translate.google.com/', '#source')

    def translate(self, text):
        self._cm.set_value('#source', text)
        time.sleep(3)
        return self._cm.get_value('span.tlid-translation.translation')


if __name__ == '__main__':
    cm = ChromeManager(driver_path=CHROME_DRIVER)
    t = Translate(cm)
    data = read_data('sentimental_analysis/sentimental_analysis_tweets.json')
    data = data[:500]
    res = []
    for d in data:
        if not d['username']:
            continue
        translated_text = t.translate(d['text'])
        res.append({
            'username': d['username'],
            'user-link': d['user-link'],
            'time': d['time'],
            'text': d['text'],
            'translated_text': translated_text,
            'tags': d['tags'],
            'location': None
        })
    save_json('sentimental_analysis/translated_tweets_1_to_5000.json', res)
    cm.close()
