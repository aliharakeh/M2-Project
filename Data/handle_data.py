import json
import os
import csv


def get_file_details(filename):
    data = read_data(filename)
    print(f'Nb. of Tweets in [{filename}] = {len(data)}')
    u = [k.split('-')[0] for k in data.keys()]
    u = {k for k in u}
    print(f'Nb. of Users in [{filename}] = {len(u)}')


def read_data(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.loads(f.read())


def save_json(filename, data):
    with open(f'{filename}.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(data, indent=2, ensure_ascii=False))


def merge_files(files_dir, result_filename):
    result = []
    files = os.listdir(files_dir)
    for file in files:
        data: dict = read_data(f'{files_dir}/{file}')
        result += list(data.values())

    save_json(result_filename, result)


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
    # merge_files('sentimental_analysis', 'sentimental_analysis/sentimental_analysis_tweets')
    # data = read_data('sentimental_analysis/sentimental_analysis_tweets.json')
    # print(len(data))  # 37072 Tweet
    json_to_csv('sentimental_analysis/sentimental_analysis_tweets',
                'sentimental_analysis/sentimental_analysis_tweets.json')
