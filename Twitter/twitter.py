from Scrapping.chrome import ChromeManager
from twitter_config import TWEETS, PROBLEM_CHARS
import csv
import re


class Twitter:
    def __init__(self, chrome_manager):
        # instance variables
        self._cm: ChromeManager = chrome_manager
        self._page_loaded = False
        self.twitter_page = None
        self.tweets = []

    def load_page(self, twitter_page):
        self.twitter_page = twitter_page
        self._page_loaded = self._cm.load_page(self.twitter_page, wait_element_selector=TWEETS['css-selector'])

    def get_some_tweets(self, tweets_count=100):
        if self._page_loaded:
            current_tweets_count = 0
            while current_tweets_count < tweets_count:
                self._cm.scroll_page(scroll_count=1)
                tweets = self._cm.get_elements(TWEETS['css-selector'])
                for tweet in tweets:
                    self.tweets.append(tweet.text)  # TODO: can replace this with Tweet() object
                    current_tweets_count += 1
                    if current_tweets_count == tweets_count:
                        break

    def get_all_tweets(self):
        if self._page_loaded:
            for _ in self._cm.scroll_page(scroll_till_end=True, external_func=True):
                tweets = self._cm.get_elements(TWEETS['css-selector'])
                for tweet in tweets:
                    self.tweets.append(tweet.text)  # TODO: can replace this with Tweet() object
                print(f'[INFO] Tweets = {len(self.tweets)}')

    def display_tweets(self):
        for index, tweet in enumerate(self.tweets):
            print(f'[Tweet {index}]')
            print(tweet)
            print('---------------------------------------------------------------------------\n')

    def save_tweets_to_csv(self):
        filename = re.sub(PROBLEM_CHARS, '_', self.twitter_page)
        with open(f'{filename}.csv', 'w', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, lineterminator='\n', delimiter=',', quotechar='"')
            for index, tweet in enumerate(self.tweets):
                writer.writerow((index, tweet))
