from selenium.webdriver.remote.webelement import WebElement
from twitter_config import CITIES_DICTIONARY, TWEET
import json
from difflib import SequenceMatcher
import re

with open(CITIES_DICTIONARY, 'r', encoding='utf-8') as f:
    Cities = json.loads(f.read())


class Tweet:
    def __init__(self, tweet_element):
        # instance variables
        self.tweet_element: WebElement = tweet_element
        self.tweet_text = ''
        self.tags = None
        self.tweet_user = None
        self.tweet_user_link = None
        self.tweet_time = None

        # parse tweet
        self.__parse_tweet()

    def __parse_tweet(self):
        self.tweet_text = self.tweet_element.find_element_by_css_selector(TWEET['text']).text
        self.tweet_user = self.tweet_element.find_element_by_css_selector(TWEET['username']).text
        self.tweet_user_link = self.tweet_element.find_element_by_css_selector(TWEET['user-link']).get_attribute('href')
        self.tweet_time = self.tweet_element.find_element_by_css_selector(TWEET['time']).text
        tags = re.search(TWEET['tags'], self.tweet_text)
        self.tags = tags.groups() if tags else None

    def __get_tweet_words(self):
        return map(lambda s: s.strip(), self.tweet_text.split(' '))

    def __check_location(self, word, ratio=0.8):
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
        if k1 in Cities and k2 in Cities[k1]:
            city_list = Cities[k1][k2]
            for city in city_list:
                city_lowercase = city.lower()
                if word == city_lowercase:
                    return city
                if SequenceMatcher(None, word, city_lowercase).ratio() >= ratio:
                    possible_city = city
        return possible_city

    def get_tweet_locations(self, ratio=0.8):
        words = self.__get_tweet_words()
        locations = {}
        for word in words:
            location = self.__check_location(word, ratio)
            if location:
                if word not in locations:
                    locations[location] = 0
                locations[location] += 1
        return sorted(locations.items(), key=lambda l: l[1], reverse=True)

    def __repr__(self):
        return (
            f'<Tweet: {self.tweet_user}>\n' +
            f'[Time]: {self.tweet_time}\n' +
            f'[User Url]: {self.tweet_user_link}\n' +
            f'[Tags]: {self.tags}\n' +
            f'[Text]: {self.tweet_text}\n' +
            '------------------------------------------'
        )
