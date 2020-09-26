
from Locations.locations import LocationParser
import twint
class TwintTweet:
    def __init__(self, t):
        self.id = t.id
        self.id_str = t.id_str
        self.conversation_id = t.conversation_id
        self.datetime = t.datetime
        self.datestamp = t.datestamp
        self.timestamp = t.timestamp
        self.user_id = t.user_id
        self.user_id_str = t.user_id_str
        self.username = t.username
        self.name = t.name
        self.place = t.place
        self.timezone = t.timezone
        self.mentions = t.mentions
        self.urls = t.urls
        self.photos = t.photos
        self.video = t.video
        self.tweet = t.tweet
        self.hashtags = t.hashtags
        self.cashtags = t.cashtags
        self.replies_count = t.replies_count
        self.retweets_count = t.retweets_count
        self.likes_count = t.likes_count
        self.link = t.link
        self.user_rt_id = t.user_rt_id
        self.user_rt = t.user_rt
        self.retweet = t.retweet
        self.retweet_id = t.retweet_id
        self.retweet_date = t.retweet_date
        self.retweet_id = t.retweet_id
        self.retweet_date = t.retweet_date
        self.quote_url = t.quote_url
        self.near = t.near
        self.geo = t.geo
        self.source = t.source
        self.reply_to = t.reply_to
        self.translate = t.translate
        self.trans_src = t.trans_src
        self.trans_dest = t.trans_dest

    def __repr__(self):
        return f'<{self.username}> <{self.datetime}> <{self.tweet}>'


class TwitterTwint:

    @staticmethod
    def search_twitter(
            username=None,
            search=None,
            limit=100,
            since=None,
            until=None,
            near=None,
            geo=None,
            csv_output=None,
            json_output=None
    ):
        """
        :param username: (string) - Twitter user's username
        :param search: (string) - Search terms
        :param limit: (int) - Number of Tweets to pull. (Increments of 20)
        :param since: (string) - Filter Tweets sent since date. (Example: 2017-12-27)
        :param until: (string) - Filter Tweets sent until date. (Example: 2017-12-27)
        :param near: (string) - Near a certain City (Example: london)
        :param csv_output: (string) - CSV Output file
        :param json_output: (string) - JSON Output file
        :return: scrapped tweets
        """
        # store in memory check
        memory_store = not csv_output and not json_output
        tweets = []

        # scrap settings
        c = twint.Config()
        c.Hide_output = True
        c.Limit = limit

        if memory_store:
            c.Store_object = True
            c.Store_object_tweets_list = tweets

        if search is not None:
            c.Search = search

        if username:
            c.Username = username

        if near:
            c.Near = near

        if geo:
            c.Geo = geo

        if since:
            c.Since = since

        if until:
            c.Until = until

        if csv_output:
            c.Store_csv = True
            c.Output = csv_output

        if json_output:
            c.Store_json = True
            c.Output = json_output

        # scarp tweets
        twint.run.Search(c)

        if memory_store:
            return [TwintTweet(tweet) for tweet in tweets]

    @staticmethod
    def predict_twitter_user_location(username, limit=2000, similarity_ratio=0.8):
        tweets = TwitterTwint.search_twitter(username=username, limit=limit)
        print(len(tweets))
        locations = {}
        for tweet in tweets:
            predicted_locations = LocationParser.get_locations(tweet.tweet, similarity_ratio)
            for location, frequency in predicted_locations:
                if location not in locations:
                    locations[location] = {
                        'frequency': frequency,
                        'tweets': [tweet.tweet]
                    }
                else:
                    locations[location]['frequency'] += frequency
                    locations[location]['tweets'].append(tweet.tweet)

        return locations
        # return sorted(locations.items(), key=lambda l: l[1], reverse=True)

if __name__ == '__main__':
    # locations = TwitterTwint.predict_twitter_user_location('waddahsadek', limit=2000, similarity_ratio=0.9)
    # with open('result.json', 'w', encoding='utf-8') as f:
    #     f.write(json.dumps(locations, indent=2, ensure_ascii=False))

    TwitterTwint.search_twitter(username='waddahsadek', limit=20, csv_output='a')