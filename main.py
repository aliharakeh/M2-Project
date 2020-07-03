from Scrapping import ChromeManager
from Twitter import Twitter
from twitter_config import CHROME_DRIVER

if __name__ == '__main__':
    cm = ChromeManager(driver_path=CHROME_DRIVER)
    tw = Twitter(cm)
    tw.load_page(
        'https://twitter.com/search?q=%23%D8%B3%D8%B9%D8%AF_%D8%A7%D9%84%D8%AD%D8%B1%D9%8A%D8%B1%D9%8A&src=trend_click')
    tw.get_some_tweets(5)
    tw.display_tweets()
    tw.save_as_json('tweets')
    cm.close()
