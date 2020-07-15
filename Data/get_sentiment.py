from textblob import TextBlob
from Data.handle_data import read_data, save_json


def get_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity


def data_sentiment(filename):
    data = read_data(filename)
    res = []
    for d in data:
        # if not d['translated_text']:
        #     print(d)
        res.append({
            **d,
            'sentiment': get_sentiment(d['translated_text'])
        })
    save_json(filename.replace('translated', 'sentimental_analysis'), res)


def get_sentiment_details(filename):
    data = read_data(filename)
    sentiments = [0, 0, 0]
    total = len(data)
    for d in data:
        if d['sentiment'] < 0:
            sentiments[0] += 1
        elif d['sentiment'] == 0:
            sentiments[1] += 1
        else:
            sentiments[2] += 1
    file = filename.split("\\")[-1]
    return (
            f'<Sentiment for {file}\n' +
            '--------------------------------------------------------\n' +
            f'[Negative]: {sentiments[0]}\n' +
            f'[Neutral]: {sentiments[1]}\n' +
            f'[Positive]: {sentiments[2]}\n' +
            f'[Total]: {total}\n' +
            '********************************************************\n'
    )


if __name__ == '__main__':
    files = [
        'sentimental_analysis\\sentimental_analysis\\#corona_lebanon_tweets_11_7_2020.json',
        'sentimental_analysis\\sentimental_analysis\\#corona_tweets_12_7_2020.json',
        'sentimental_analysis\\sentimental_analysis\\healthcare_tweets_10_7_2020.json',
        'sentimental_analysis\\sentimental_analysis\\medical_tweets_11_7_2020.json',
    ]

    for file in files:
        # data_sentiment(file)
        print(get_sentiment_details(file))
