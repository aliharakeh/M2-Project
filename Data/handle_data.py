import json
import os
import csv


def get_tweet_count(filename):
    data = read_data(filename)
    return len(data)


def read_data(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.loads(f.read())


def save_json(filename, data):
    filename = filename.replace('.json', '')
    with open(f'{filename}.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(data, indent=2, ensure_ascii=False))


def merge_files(files_dir, result_filename):
    result = []
    files = os.listdir(files_dir)
    for file in files:
        data: dict = read_data(f'{files_dir}/{file}')
        result += list(data.values())

    save_json(result_filename, result)


def clean_file(filename, data_file):
    data = read_data(data_file)
    res = []
    for d in data.values():
        # remove None and reply tweets
        if not d['username'] or 'replying to' in d['text'].lower():
            continue
        # remove inner html
        del d['innerHTML']
        res.append(d)
    save_json(filename, res)


def json_to_csv(filename, data_file):
    data = read_data(data_file)
    with open(f'{filename}.csv', 'w', newline='', encoding='utf-8') as f:
        wr = csv.writer(f)
        for d in data:
            if not d['username']:
                continue
            wr.writerow([
                d['username'],
                d['user-link'],
                d['time'],
                d['text'].replace('\n', ' '),
                ';'.join(d['tags']) if len(d['tags']) > 0 else 'None'
            ])


if __name__ == '__main__':
    # files = [
    #     '#corona_lebanon_tweets_11_7_2020.json',
    #     '#corona_tweets_12_7_2020.json',
    #     'healthcare_tweets_10_7_2020.json',
    #     'medical_tweets_11_7_2020.json'
    # ]

    # merge_files('sentimental_analysis', 'sentimental_analysis/sentimental_analysis_tweets')
    # data = read_data('sentimental_analysis/sentimental_analysis_tweets.json')
    # print(len(data))  # 37072 Tweet

    # json_to_csv('sentimental_analysis/sentimental_analysis_tweets',
    #             'sentimental_analysis/sentimental_analysis_tweets.json')

    # for file in files:
    #     clean_file(f'sentimental_analysis/without_html/{file.replace(".json", "")}',
    #                f'sentimental_analysis/with_html/{file}')

    # total = 0
    # for file in files:
    #     total += get_tweet_count(f'sentimental_analysis/with_html/{file}')
    # print(total)  # 37,072
    # files = [
    #     'sentimental_analysis\\#corona_lebanon_tweets_11_7_2020_range_0_5000.json',
    #     'sentimental_analysis\\#corona_lebanon_tweets_11_7_2020_range_5000_10000.json',
    #     'sentimental_analysis\\#corona_lebanon_tweets_11_7_2020_range_10000_12500.json',
    #     'sentimental_analysis\\#corona_lebanon_tweets_11_7_2020_range_12500_15673.json'
    # ]
    # res = []
    # for file in files:
    #     res += read_data(file)
    # save_json('sentimental_analysis\\translated\\#corona_lebanon_tweets_11_7_2020.json', res)
    pass
