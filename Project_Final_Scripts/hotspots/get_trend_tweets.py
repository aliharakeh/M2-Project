from Scrapping import BeautifulSoupScrape as BSS
import json

if __name__ == '__main__':
    # read data
    with open('hotspots_topics_trends.json', encoding='utf-8') as f:
        hotspots = json.loads(f.read())

    # get tweets
    for _, hotspot in hotspots.items():

        for trend in hotspot['trends']:

            # pager data
            pager_data = BSS.get_elements('center:nth-child(3) > nav > ul > li', source=trend['link'], attributes=True)
            max_page = len(pager_data) - 2
            pages_range = range(max_page)

            # pages links
            tweets_pages = [f'{trend["link"]}/{page + 1}' for page in pages_range]

            # tweets
            tweets = []
            for tweets_page in tweets_pages:
                tweets += [
                    el['text'] for el in
                    BSS.get_elements('div > div.panel-body > p', source=tweets_page, attributes=True)
                ]

            # save
            trend['tweets'] = tweets

    # save data
    with open('hotspots.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(hotspots, indent=2, ensure_ascii=False))
