from selenium.webdriver.remote.webelement import WebElement
from Scrapping.beautiful_soup import BeautifulSoupScrap as BSC
from twitter_config import CITIES_DICTIONARY
import json
from difflib import SequenceMatcher

with open(CITIES_DICTIONARY, 'r', encoding='utf-8') as f:
    Cities = json.loads(f.read())


class Tweet:
    def __init__(self, tweet_element):
        # instance variables
        # self.tweet_element: WebElement = tweet_element
        # self.tweet_bs4 = BSC.get_bs4_from_html(tweet_element)
        self.tweet_text = tweet_element  # tweet_element.text
        self.tags = None
        self.tweet_user = None
        self.tweet_user_link = None

    def __get_tweet_words(self):
        return map(lambda s: s.strip(), self.tweet_text.split(' '))

    def __check_location(self, word):
        if len(word) < 2:
            return None
        word = word.lower()
        k1 = word[0]
        k2 = word[1]
        if k1 in Cities and k2 in Cities[k1]:
            city_list = Cities[k1][k2]
            for city in city_list:
                # This ratio value helps getting the real locations and some predicted ones if the 2 keys are available
                # Real Locations have ratio >= 0.8
                # Ratio of 0.6 gets us some predicted locations:
                # ex: word = saw
                #     --> k1 = s, k2 = a
                #     --> Cities['s']['a'] = [..., 'Sawfar']
                #     --> SequenceMatcher(None, 'saw', 'Sawfar').ratio() >= 0.6
                #     --> predicted location = 'Sawfar'
                if SequenceMatcher(None, word, city.lower()).ratio() >= 0.6:
                    return city
        return None

    def get_tweet_locations(self):
        words = self.__get_tweet_words()
        locations = {}
        for word in words:
            location = self.__check_location(word)
            if location:
                if word not in locations:
                    locations[location] = 0
                locations[location] += 1
        return locations


if __name__ == '__main__':
    t = Tweet('We were going to Verdun when we saw Verdun before us, but then we went to Fghal to see Fourate and Bakka')
    ls = t.get_tweet_locations()
    for l, v in ls.items():
        print(f'{l} ==> {v}')
