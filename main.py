from Scrapping import ChromeManager
from Twitter import Twitter
from twitter_config import CHROME_DRIVER
import json

if __name__ == '__main__':
    # cm = ChromeManager(driver_path=CHROME_DRIVER)
    # tw = Twitter(cm)
    # tw.load_page('https://twitter.com/search?q=corona&src=typed_query&lf=on')
    # links = [
    #     'corona until:2020-06-01 since:2020-05-01'
    # ]
    # input('Configure Twitter setting then enter any key to continue...\n--> ')
    # try:
    #     tw.get_all_tweets()
    # except Exception as e:
    #     print(e)
    #     print(f'[Error] => saved {len(tw.tweets)} tweets')
    # finally:
    #     print('DONE!!')
    #     tw.save_as_json('Data/corona_latest_2020_tweets')
    # cm.close()

    with open('Data/corona_latest_2020_tweets.json', 'r', encoding='utf-8') as f:
        d = json.loads(f.read())

    print(len(d))  # 2046 tweets
    u = [k.split('-')[0] for k in d.keys()]
    u = {k for k in u}
    print(len(u))  # 2018 user
