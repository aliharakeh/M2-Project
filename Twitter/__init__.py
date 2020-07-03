from .twitter import Twitter
from .twitter_user import TwitterUser
from .tweet import TweetParser
from twitter_config import CITIES_DICTIONARY


def load_cities():
    import json
    with open(CITIES_DICTIONARY, 'r', encoding='utf-8') as cities:
        TweetParser.Cities = json.loads(cities.read())
