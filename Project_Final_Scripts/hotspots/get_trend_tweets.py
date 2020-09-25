from Scrapping import BeautifulSoupScrape as BSS
import json
import time

if __name__ == '__main__':
    # read data
    with open('hotspots_topics_trends.json', encoding='utf-8') as f:
        hotspots = json.loads(f.read())

    # get tweets
    for _, hotspot in hotspots.items():

        print('Processing', hotspot['date'], '...')

        for trend in hotspot['trends']:

            # for updating and not first time use of this code
            # if len(trend['tweets']) > 0:
            #     continue

            # pager data
            pager_data = BSS.get_elements('center:nth-child(3) > nav > ul > li', source=trend['link'], attributes=True)
            max_page = len(pager_data) - 2
            pages_range = range(max_page)

            # pages links
            tweets_pages = [f'{trend["link"]}/{page + 1}' for page in pages_range]

            # tweets
            print('Getting Tweets...')
            tweets = []
            for tweets_page in tweets_pages:
                tweets += [
                    el['text'] for el in
                    BSS.get_elements('div > div.panel-body > p', source=tweets_page, attributes=True)
                ]

                # delay next request a little
                time.sleep(0.5)

            # save
            print(len(tweets), 'Tweets were scraped!!', )
            trend['tweets'] = [tweet for tweet in set(tweets) if tweet]

        print('-------------------------------------------------------')

    # save data
    print('Saving...')
    with open('hotspots.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(hotspots, indent=2, ensure_ascii=False))

    print('Done!!')
