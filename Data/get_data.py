from Scrapping import ChromeManager
from Twitter import Twitter
from twitter_config import CHROME_DRIVER

if __name__ == '__main__':
    cm = ChromeManager(driver_path=CHROME_DRIVER)
    tw = Twitter(cm)
    tw.load_page('https://twitter.com/search?q=medical%20lebanon&src=typed_query&f=live')
    input('Configure Twitter setting then enter any key to continue...\n--> ')
    try:
        tw.get_all_tweets()
    except Exception as e:
        print(e)
        print(f'[Error] => saved {len(tw.tweets)} tweets')
    finally:
        print('DONE!!')
        tw.save_as_json('Data/#corona_tweets_12_7_2020')
    cm.close()