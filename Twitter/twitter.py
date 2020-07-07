from Scrapping.chrome import ChromeManager
from twitter_config import TWEETS
from Twitter.tweet import TweetParser
import json
import time


class Twitter:
    def __init__(self, chrome_manager):
        # instance variables
        self._cm: ChromeManager = chrome_manager
        self._page_loaded = False
        self.twitter_page = None
        self.tweets = {}

    def load_page(self, twitter_page):
        self.twitter_page = twitter_page
        self._page_loaded = self._cm.load_page(self.twitter_page, wait_element_selector=TWEETS['css-selector'])

    def __save_tweet(self, tweet, include_locations):
        """
        Tweet Details Choices:
        ---------------------
            - TweetParser.parse_tweet(tweet)
            - tweet.text
            - tweet.get_attribute('innerHTML')
            - tweet.get_attribute('outerHTML')

        * Note: Can be overridden when used in inheritance
        """
        details = TweetParser.parse_tweet(tweet, include_locations)
        key = f'{details["username"]}_{details["time"]}'
        if key == 'None_None':
            key = f'{len(self.tweets)}_{key}'
        self.tweets[key] = details

    def get_some_tweets(self, tweets_count=100, include_locations=False):
        if self._page_loaded:
            current_tweets_count = 0
            while current_tweets_count < tweets_count:
                self._cm.scroll_page(scroll_count=1)
                tweets = self._cm.get_elements(TWEETS['css-selector'])
                for tweet in tweets:
                    self.__save_tweet(tweet, include_locations)
                    current_tweets_count += 1
                    if current_tweets_count == tweets_count:
                        break

    def get_all_tweets(self, include_locations=False):
        if self._page_loaded:
            for _ in self._cm.scroll_page(scroll_till_end=True, external_func=True, scroll_delay_sec=30):
                tweets = self._cm.get_elements(TWEETS['css-selector'])
                for tweet in tweets:
                    self.__save_tweet(tweet, include_locations)
                print(f'[INFO] Tweets = {len(self.tweets)}')

    def display_tweets(self):
        for index, tweet in enumerate(self.tweets):
            print(f'[Tweet {index}]')
            print(tweet)

    def save_as_json(self, filename):
        with open(f'{filename}.json', 'w', encoding='utf-8') as file:
            file.write(json.dumps(self.tweets, indent=2, ensure_ascii=False))
