from chrome import ChromeManager
from Twitter_Config import TWITTER_USER, TWEET, RETWEET


class Tweet:
    tweet_element = None
    tweet_content = None
    retweet_content = None
    quote_content = None
    tags = None

    def __init__(self, tweet_element):
        self.tweet_element = tweet_element


class TwitterUser:
    # non-public variables
    _cm: ChromeManager = None
    _page_loaded = False

    # user info
    username = None
    public_username = None
    twitter_url = None
    public_location = None
    analysed_location = None
    tweets = []

    def __init__(self, chrome_manager, twitter_url):
        # initialize driver and load user twitter page
        self._cm = chrome_manager
        self._load_user_twitter_page(twitter_url)

        # fill user info
        self.username = '@' + twitter_url.split('/')[-1]
        self.public_username = self._get_user_info(TWITTER_USER['public_username'])
        self.public_location = self._get_user_info(TWITTER_USER['public_location'])

    def _load_user_twitter_page(self, url):
        self.twitter_url = url
        self._page_loaded = self._cm.load_page(url, wait_element_selector=TWITTER_USER['tweets'])

    def _get_user_info(self, selector):
        if self._page_loaded:
            return self._cm.get_elements(selector, single_element=True).text.strip()
        return None

    def get_user_tweets(self, tweets_count=100):
        if self._page_loaded:
            current_tweets_count = 0
            while current_tweets_count < tweets_count:
                self._cm.scroll_page(scroll_count=1)
                tweets = self._cm.get_elements(TWEET_USER['tweets'])
                for tweet in tweets:
                    self.tweets.append(Tweet(tweet))
                    current_tweets_count += 1

    def __repr__(self):
        return (
                '<' +
                f'User: {self.public_username} - {self.username} / ' +
                f'Location: {self.public_location} / ' +
                f'Tweets: {len(self.tweets)} / ' +
                f'Url: {self.twitter_url}'
                '>'
        )


if __name__ == '__main__':
    _cm = ChromeManager()
    user = TwitterUser(_cm, 'https://twitter.com/noun_salah')
    # user.get_user_tweets()
    # user.get_user_public_location()
    print(user)
    print('---------')
