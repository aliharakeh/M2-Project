import json
from Language.language_utils import LanguageUtil
import os
import time

DIR = os.path.dirname(__file__)

stopwords = []
with open(f'{DIR}\\..\\..\\stop-words\\english.txt', encoding='utf-8') as f:
    stopwords += f.read().split('\n')

with open(f'{DIR}\\..\\..\\stop-words\\arabic.txt', encoding='utf-8') as f:
    stopwords += f.read().split('\n')

if __name__ == '__main__':
    with open('hotspots.json', encoding='utf-8') as f:
        hotspots = json.loads(f.read())

    final_hotspots = {}
    lu = LanguageUtil()
    count = 0

    for date, hotspot in hotspots.items():
        final_hotspots[date] = {
            **hotspot,
            'trends': []
        }
        for trend in hotspot['trends']:

            tweets = []
            for tweet in list(set(trend['tweets'])):
                if tweet:
                    tweet = " ".join([w for w in tweet.split() if w not in stopwords])
                    tweets.append(lu.quick_translation(tweet)['translated'])
                    time.sleep(1)
                    count += 1
                    print(f'translated tweet {count}')

            final_hotspots[date]['trends'].append({
                'topic': trend['topic'],
                'link': trend['link'],
                'tweets': tweets
            })

    with open('hotspots_cleaned.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(final_hotspots, indent=2, ensure_ascii=False))
