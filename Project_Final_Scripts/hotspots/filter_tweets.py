from Language.lang_detection.lang_words import is_arabic, is_english
import re
import json

WORDS = ['corona', 'كورونا', '_', 'covid', 'http']


def within_removed_words(word):
    for w in WORDS:
        if w in word:
            return True
    return False


if __name__ == '__main__':
    total_count = 0
    tweets_count = 0
    allowed_words = set()
    with open('hotspots_tweets.json', encoding='utf-8') as f:
        hotspots = json.loads(f.read())
        for date, hotspot in hotspots.items():
            for trend in hotspot['trends']:
                for tweet in list(set(trend['tweets'])):
                    if tweet:
                        tweets_count += 1
                        words = tweet.strip().split()
                        total_count += len(words)
                        for word in words:
                            if word:
                                word = re.sub(r'\W|\d', '', word)
                                if is_arabic(word) or is_english(word) or within_removed_words(word):
                                    continue
                                allowed_words.add(word)

    print(f'total tweets: {tweets_count:,}')
    print(f'total words: {total_count:,}')
    print(f'allowed words count: {len(allowed_words):,}')
    print(f'percentage: {len(allowed_words) / total_count * 100}')
    print(allowed_words)
