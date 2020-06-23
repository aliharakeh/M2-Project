from twitter_config import TWITTER_USER
from .twitter import Twitter


class TwitterUser(Twitter):
    def __init__(self, chrome_manager, user_twitter_url):
        # call super method
        super().__init__(chrome_manager)

        # load twitter page
        self.load_page(self.twitter_page)

        # user variables
        self.username = '@' + user_twitter_url.split('/')[-1]
        self.public_username = self._get_user_info(TWITTER_USER['public_username'])
        self.public_location = self._get_user_info(TWITTER_USER['public_location'])
        self.analysed_location = None

    def _get_user_info(self, selector):
        if self._page_loaded:
            element = self._cm.get_elements(selector, single_element=True)
            return element.text.strip() if element else element
        return None

    def _get_analysed_location(self):
        pass

    def __repr__(self):
        return (
                '<' +
                f'User: {self.public_username} - {self.username} / ' +
                f'Location: {self.public_location} / ' +
                f'Tweets: {len(self.tweets)} / ' +
                f'Url: {self.tweets}'
                '>'
        )
