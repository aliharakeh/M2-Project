from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from twitter_config import TWEET, CITIES_JSON
import re
from Twitter.locations import LocationParser


class TweetParser:
    @staticmethod
    def get(tweet_element: WebElement, selector, attribute_name):
        try:
            e = tweet_element.find_element_by_css_selector(selector)
            return e.get_attribute(attribute_name) if attribute_name != 'text' else e.text
        except NoSuchElementException:
            return None

    @staticmethod
    def parse_tweet(tweet_element, include_locations=True):
        tweet_text = TweetParser.get(tweet_element, TWEET['text'], 'text')

        tweet_tags = []
        if tweet_text:
            tags = re.findall(TWEET['tags'], tweet_text)
            tweet_tags = list({tag for tag in tags})

        locations = None
        if include_locations:
            LocationParser.load_locations(CITIES_JSON)
            locations = LocationParser.get_locations(tweet_text)

        return {
            'username': TweetParser.get(tweet_element, TWEET['username'], 'text'),
            'user-link': TweetParser.get(tweet_element, TWEET['user-link'], 'href'),
            'time': TweetParser.get(tweet_element, TWEET['time'], 'text'),
            'text': tweet_text,
            'tags': tweet_tags,
            'innerHTML': tweet_element.get_attribute('innerHTML'),
            'locations': locations
        }
