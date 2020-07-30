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
            search=search[0],
            limit=20,
            since='2020-1-1',
            until='2020-8-1',
            near='Lebanon',
            csv_output='Data_v2\\' + search[0].replace('#', '')
        )
