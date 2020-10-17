from Project_Final_Scripts.Locations.locations import LocationFinder, Methods
import pandas as pd

LF = LocationFinder()
count = 0
total = 0


def check_locations(text):
    global count

    locations = LF.search_text(text, method={'ar': Methods.EDIT_DISTANCE, 'en': Methods.SOUND})

    count += 1
    if count % 10 == 0:
        print(count, '/', total)

    if locations:
        res = [l for l, r in locations[:5]]
        return " | ".join(res)
    return None


if __name__ == '__main__':
    df = pd.read_csv("..\\tweets_sentiment.csv", header=0)
    total = 1000
    df = df.loc[:total].copy()
    df['locations'] = df.text.apply(check_locations)
    df.to_csv('lcoations_tweets.csv')
