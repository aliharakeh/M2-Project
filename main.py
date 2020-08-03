from Twitter import TwitterTwint

if __name__ == '__main__':
    searches = [
        'corona',
        'covid-19',
        'كورونا',
        'كورونا_لبنان',
        'healthcare',
        'medical'
    ]
    for search in searches:
        TwitterTwint.search_twitter(
            search=search,
            limit=50000,
            since='2020-1-1 0:0:0',
            geo='33.870137,35.778745,10km',
            csv_output='Data3'  # _v2\\' + search[0].replace('#', '')
        )
