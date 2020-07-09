from twitter_config import TWITTER_USER
from Twitter.twitter import Twitter


class TwitterUser(Twitter):
    def __init__(self, chrome_manager, user_twitter_url):
        # call super method
        super().__init__(chrome_manager)

        # load twitter page
        self.load_page(self.twitter_page)

        # user variables
        self.username = '@' + user_twitter_url.split('/')[-1]
        self.user_link = user_twitter_url
        self.public_username = self._get_user_info(TWITTER_USER['public_username'])
        self.public_location = self._get_user_info(TWITTER_USER['public_location'])
        self.analysed_locations = []

        # get locations and clean tweets data
        self._get_analysed_locations()
        self.tweets = {}

    def _get_user_info(self, selector):
        if self._page_loaded:
            element = self._cm.get_elements(selector, single_element=True)
            return element.text.strip() if element else element
        return None

    def _get_analysed_locations(self):
        self.get_some_tweets(tweets_count=200, include_locations=True)
        locations = {}
        tweets = self.tweets.values()
        for tweet in tweets:
            for location, frequency in tweet['locations']:
                if location not in locations:
                    locations[location] = frequency
                else:
                    locations[location] += frequency
        self.analysed_locations = sorted(locations.items(), key=lambda l: l[1], reverse=True)[:5]

    def __repr__(self):
        title = f'<User: {self.public_username} - {self.username} >'
        divider = '-' * len(title)
        return (
                f'{title}\n' +
                f'{divider}\n' +
                f'[Public Location]: {self.public_location}\n' +
                f'[Tweets]: {len(self.tweets)}\n' +
                f'[Url]: {self.tweets}\n' +
                f'[Possible Locations]: {self.analysed_locations}\n' +
                '*************************************************************'
        )
