from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from twitter_config import TWEET, PROBLEM_CHARS
from difflib import SequenceMatcher
import re


class TweetParser:
    Cities = {}

    @staticmethod
    def get_attribute_from_selector(tweet_element: WebElement, selector, attribute_name):
        try:
            e = tweet_element.find_element_by_css_selector(selector)
            return e.get_attribute(attribute_name) if attribute_name != 'text' else e.text
        except NoSuchElementException:
            return None

    @staticmethod
    def get_tweet_words(text):
        text = re.sub(PROBLEM_CHARS, '', text)
        return map(lambda s: s.strip(), text.split(' '))

    @staticmethod
    def check_and_get_location(word, ratio=0.8):
        """
        This ratio value helps getting the real locations and some predicted ones if the 2 keys are available
        Real Locations have ratio >= 0.8
        Ratio of 0.6 gets us some predicted locations:
        example:
            --> word = saw
            --> k1 = s, k2 = a
            --> Cities['s']['a'] = [..., 'Sawfar']
            --> SequenceMatcher(None, 'saw', 'Sawfar').ratio() >= 0.6
            --> predicted location = 'Sawfar'
        """
        if len(word) < 2:
            return None
        word = word.lower()
        k1 = word[0]
        k2 = word[1]
        possible_city = None
        if k1 in TweetParser.Cities and k2 in TweetParser.Cities[k1]:
            city_list = TweetParser.Cities[k1][k2]
            for city in city_list:
                city_lowercase = city.lower()
                if word == city_lowercase:
                    return city
                if SequenceMatcher(None, word, city_lowercase).ratio() >= ratio:
                    possible_city = city
        return possible_city

    @staticmethod
    def get_tweet_locations(tweet_text, ratio=0.8):
        words = TweetParser.get_tweet_words(tweet_text)
        locations = {}
        for word in words:
            location = TweetParser.check_and_get_location(word, ratio)
            if location:
                if word not in locations:
                    locations[location] = 0
                locations[location] += 1
        return sorted(locations.items(), key=lambda l: l[1], reverse=True)

    @staticmethod
    def parse_tweet(tweet_element, include_locations=True):
        tweet_text = TweetParser.get_attribute_from_selector(tweet_element, TWEET['text'], 'text')

        tweet_tags = []
        if tweet_text:
            tags = re.findall(TWEET['tags'], tweet_text)
            tweet_tags = list({tag for tag in tags})

        locations = None
        if include_locations:
            locations = TweetParser.get_tweet_locations(tweet_text)

        return {
            'username': TweetParser.get_attribute_from_selector(tweet_element, TWEET['username'], 'text'),
            'user-link': TweetParser.get_attribute_from_selector(tweet_element, TWEET['user-link'], 'href'),
            'time': TweetParser.get_attribute_from_selector(tweet_element, TWEET['time'], 'text'),
            'text': tweet_text,
            'tags': tweet_tags,
            'innerHTML': tweet_element.get_attribute('innerHTML'),
            'locations': locations
        }
