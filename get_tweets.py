from chrome import ChromeManager


class TwitterUser:
    # non-public variables
    _cm: ChromeManager = None
    _page_loaded = False
    _css_selectors = {
        'public_username': 'div#react-root div.css-1dbjc4n.r-1g94qm0 > div > div > div.css-1dbjc4n.r-1awozwy.r-18u37iz.r-dnmrzs > div > span:nth-child(1) > span',
        'public_location': 'div#react-root div > span:nth-child(1) > span > span',
        'tweets': 'article'
    }

    # user info
    username = None
    public_username = None
    twitter_url = None
    tweets = []
    public_location = None

    def __init__(self, chrome_manager, twitter_url):
        # initialize driver and load user twitter page
        self._cm = chrome_manager
        self._load_user_twitter_page(twitter_url)

        # fill user info
        self.username = '@' + twitter_url.split('/')[-1]
        self.public_username = self._get_user_info(self._css_selectors['public_username'])
        self.public_location = self._get_user_info(self._css_selectors['public_location'])

    def _load_user_twitter_page(self, url):
        self.twitter_url = url
        self._page_loaded = self._cm.load_page(url, 'article')

    def _get_user_info(self, selector):
        if self._page_loaded:
            return self._cm.get_elements(selector, single_element=True).text.strip()

    def _get_tweet_details(self, tweet_element):
        pass

    def get_user_tweets(self, tweets_count=100):
        if self._page_loaded:
            current_tweets_count = 0
            while current_tweets_count < tweets_count:
                self._cm.scroll_page(scroll_count=1)
                tweets = self._cm.get_elements(self._css_selectors['tweets'])
                for tweet in tweets:
                    self.tweets.append(self._get_tweet_details(tweet))
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
