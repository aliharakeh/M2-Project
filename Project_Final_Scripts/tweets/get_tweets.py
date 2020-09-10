from Scrapping import ChromeManager
from Twitter import TwitterScrapper

URL = 'https://twitter.com/search?f=live&q=covid-19%20since%3A2020-07-31&src=typed_query&lf=on'
SAVE_FILE = 'covid_tweets_1_8_2020+'

if __name__ == '__main__':
    cm = ChromeManager()
    tw = TwitterScrapper(cm)
    tw.load_page(URL)
    input('Configure Twitter setting then enter any key to continue...\n--> ')

    try:
        tw.get_all_tweets()

    except Exception as e:
        print(e)
        print(f'[Error] => saved {len(tw.tweets)} tweets')

    finally:
        print('DONE!!')
        tw.save_as_csv(SAVE_FILE)
        cm.close()
