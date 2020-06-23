from Scrapping import ChromeManager
from Twitter import TwitterUser
from twitter_config import CHROME_DRIVER

if __name__ == '__main__':
    cm = ChromeManager(driver_path=CHROME_DRIVER)
    user = TwitterUser(cm, 'https://twitter.com/search?q=abb%20until%3A2016-12-28%20since%3A2016-12-27&src=typed_query')
    # user.get_some_tweets(tweets_count=10)
    # user.display_tweets()
    # print(user)
    user.get_all_tweets()
    user.save_tweets_to_csv()
    cm.close()
