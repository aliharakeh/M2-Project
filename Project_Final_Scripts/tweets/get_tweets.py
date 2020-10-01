from Twitter import TwitterScrapper

keywords = [
    'corona lebanon',
    'covid lebanon',
    'كورونا',
    'كورونا_لبنان',
    'healthcare lebanon',
    'medical lebanon'
]
since = '2020-09-06'
search = 'medical lebanon'
URL = f'https://twitter.com/search?q={search}%20since%3A{since}&src=typed_query&f=live'
SAVE_FILE = f'..\\combine_dataFrames\\tweets_{search}_6_9_2020+'

if __name__ == '__main__':
    tw = TwitterScrapper()
    tw.load_page(URL)
    input_ = input('Configure Twitter setting then enter any key to continue...\n--> ')

    try:
        tw.get_all_tweets()

    except Exception as e:
        print(e)
        print(f'[Error] => saved {len(tw.tweets)} tweets')

    finally:
        print('DONE!!')
        tw.save_as_csv(SAVE_FILE)
