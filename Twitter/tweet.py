from selenium.webdriver.remote.webelement import WebElement


class Tweet:
    def __init__(self, tweet_element):
        # instance variables
        self.tweet_element: WebElement = tweet_element
        self.tweet_content = tweet_element.text
        self.retweet_content = None
        self.quote_content = None
        self.tags = None

    def parse_tweet(self):
        spans = self.tweet_element.find_elements_by_tag_name('span')
        for span in spans:
            self.tweet_content.append(span.text)
