import re
import json
from fuzzywuzzy import fuzz
import jellyfish
import functools
import os

PROBLEM_CHARS = r'[\[=\+/&<>;:!\\|*^\'"\?%$@)(_\,\.\t\r\n0-9-—\]]'
ARABIC_REGEX = '[\u0621-\u064A]+'
EN_ALPHANUMERIC = 'abcdefghijklmnopqrstuvwxyz123456789 \t\n'
LOCAL_DIR = os.path.dirname(__file__)


# decorator to load details data when needed only
def load_details(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            if not LocationParser.Cities_Details:
                LocationParser.load_locations_details()

            return func(*args, **kwargs)

        except FileNotFoundError:
            print('[Error]: Data File(s) Not Found!! Please Load Data Manually')

    return wrapper


class LocationParser:
    Cities = None
    Cities_Details = None

    def __init__(self):
        self.load_locations()

    @staticmethod
    def load_locations(cities_json=f'{LOCAL_DIR}\\cities.json'):
        if LocationParser.Cities is None:
            with open(cities_json, 'r', encoding='utf-8') as cities_file:
                LocationParser.Cities = json.loads(cities_file.read())

    @staticmethod
    def load_locations_details(cities_json=f'{LOCAL_DIR}\\cities_details.json'):
        if LocationParser.Cities_Details is None:
            with open(cities_json, 'r', encoding='utf-8') as cities_file:
                LocationParser.Cities_Details = json.loads(cities_file.read())

    def __is_english(self, word):
        for char in word:
            if char not in EN_ALPHANUMERIC:
                return False
        return True

    def get_words_lists(self, text):
        """
        cleans the text from any problem chars and return 2 lists each representing arabic and english words respectively. \n
        PROBLEM_CHARS = '[\[=\+/&<>;:!\\|*^\'"\?%$@)(_\,\.\t\r\n0-9-—\]]'
        """
        text = re.sub(PROBLEM_CHARS, '', text)
        words = text.split()
        en = []
        others = []
        for word in words:
            if self.__is_english(word):
                en.append(word)
            else:
                others.append(word)
        return en, others

    @classmethod
    def __get_location_details(cls, location):
        return cls.Cities_Details.get(location, None)

    @classmethod
    def get_locations_list(cls, lang=None):
        """
        return a list of locations.\n
        can be:
        - lang = None --> all locations
        - lang = 'en' --> locations in english
        - lang = 'ar' --> locations in arabic
        """
        res = []
        for k, v in cls.Cities.items():

            # exclude non english when lang == 'en'
            if (lang == 'en') and (k not in EN_ALPHANUMERIC):
                continue

            # exclude english when lang == 'ar'
            if (lang == 'ar') and (k in EN_ALPHANUMERIC):
                continue

            for k1, v1 in v.items():
                res += v1

        return res

    def predict_location_by_pronunciation(self, word, similarity_ratio=80):
        """
        returns the exact location name or the best predicted/possible location name if there was any match,
        else returns None
        """
        if len(word) <= 2:
            return None, -1

        # initialize
        word = word.lower()
        best_predicted = (None, -1)  # (location, similarity_ratio)

        # check possible locations
        locations = LocationParser.get_locations_list(lang='en')
        for location in locations:
            # check exact location name
            if location == word:
                return location, 100

            # get sound encoding and similarity ratio
            word_sound = jellyfish.soundex(word)
            location_sound = jellyfish.soundex(location)
            local_similarity_ratio = fuzz.ratio(word, location)

            # conditions
            first_prediction = best_predicted[1] == -1
            accepted_prediction = (word_sound == location_sound) and (local_similarity_ratio >= similarity_ratio)
            better_prediction = local_similarity_ratio > best_predicted[1]

            # update prediction
            if accepted_prediction and (first_prediction or better_prediction):
                best_predicted = (location, local_similarity_ratio)

        return best_predicted

    def predict_location_by_edit_ratio(self, word, lang=None, similarity_ratio=80):
        """
        returns the exact location name or the best predicted/possible location name if there was any match,
        else returns None
        """
        if len(word) <= 2:
            return None, -1

        # initialize
        word = word.lower()
        best_predicted = (None, -1)  # (location, similarity_ratio)

        # check possible locations
        locations = LocationParser.get_locations_list(lang=lang)
        for location in locations:
            # check exact location name
            if location == word:
                return location, 100

            # get similarity ratio
            partial_ratio = fuzz.partial_ratio(word, location)
            ratio = fuzz.ratio(word, location)
            local_similarity_ratio = (partial_ratio + ratio) / 2

            # conditions
            first_prediction = best_predicted[1] == -1
            accepted_prediction = local_similarity_ratio >= similarity_ratio
            better_prediction = local_similarity_ratio > best_predicted[1]

            # update prediction
            if accepted_prediction and (first_prediction or better_prediction):
                best_predicted = (location, local_similarity_ratio)

        return best_predicted

    def predict_location(self, word, lang=None, by_pronunciation=False, similarity_ratio=80):
        """
        returns the predicted location.\n
        """
        if by_pronunciation:
            return self.predict_location_by_pronunciation(word, similarity_ratio)
        return self.predict_location_by_edit_ratio(word, lang, similarity_ratio)

    def parse_locations_in_text(self, words, lang=None, by_pronunciation=False, similarity_ratio=80):
        locations = []
        for word in words:
            locations.append(self.predict_location(word, lang, by_pronunciation, similarity_ratio))
        return locations

    def get_locations(self, text, by_pronunciation=False, similarity_ratio=80):
        """
        returns a descending sorted list of location tuples containing the location name and its frequency
        found in the provided text
        """
        # get words list
        en, ar = self.get_words_lists(text)
        en_locations = ar_locations = []

        # predict locations
        if en:
            en_locations = self.parse_locations_in_text(en, 'en', by_pronunciation, similarity_ratio)

        if ar:
            ar_locations = self.parse_locations_in_text(ar, 'ar', False, similarity_ratio)

        # combine results
        locations = [
            *en_locations,
            *ar_locations
        ]

        # return a descending sorted list of tuples containing the location name and it's frequency
        return sorted(locations, key=lambda l: l[1], reverse=True)

    @load_details
    def get_location_details(self, location, predict=True):
        """
        returns a location details
        Note: It predicts the location if it was not found.
        """
        # get location data
        location = location.lower()
        location_data = self.__get_location_details(location)

        # if location is not found, check if it refers to a location and get its data
        if not location_data and predict:
            location = self.predict_location(location)
            return self.__get_location_details(location)

        return location_data

    @load_details
    def get_location_aliases(self, location, predict=True):
        """
        returns the other aliases of a location
        Note: It predicts the location if it was not found.
        """
        location_data = self.get_location_details(location, predict)

        # combine the aliases
        res = []
        latin = location_data.get('latin', None)
        non_latin = location_data.get('non-latin', None)
        if latin:
            res += latin
        if non_latin:
            res += non_latin

        # return unique aliases
        return list(set(res))

    @load_details
    def get_arabic_alias(self, location, predict=True):
        """
        returns the arabic aliases of a location.  \n
        Note: It predicts the location if it was not found.
        """
        aliases = self.get_location_aliases(location, predict)
        for alias in aliases:
            if re.search(ARABIC_REGEX, alias):
                return alias
        return None


if __name__ == '__main__':
    lp = LocationParser()

    # print(len(lp.get_locations_list()))
    # print(len(lp.get_locations_list(lang='en')))
    # print(len(lp.get_locations_list(lang='ar')))

    # location = lp.predict_location('beyrout')
    # print(location)
    # location = lp.predict_location('البيروت')
    # print(location)

    # print(jellyfish.soundex('akka'))
    # print(jellyfish.soundex('akkar'))
    # print(fuzz.partial_ratio('aandkit', 'and'))
    # print(fuzz.ratio('aandkit', 'and'))
    # print(fuzz.partial_ratio('where', 'hereh'))
    # print(fuzz.ratio('where', 'hereh'))
    # print(fuzz.partial_ratio('akka', 'akkar'))
    # print(fuzz.ratio('akka', 'akkar'))

    locations = lp.get_locations('Hello, I\'m from baabda where Aakka live in beirut and beirut')
    for l in locations:
        print(l)



