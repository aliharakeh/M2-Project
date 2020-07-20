import json
import os
import csv


def get_file_data_count(filename):
    data = read_data(filename)
    return len(data)


def read_data(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.loads(f.read())


def save_json(filename, data):
    filename = filename.replace('.json', '')
    with open(f'{filename}.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(data, indent=2, ensure_ascii=False))


def merge_files_dicts(files_dir, result_filename):
    result = []
    files = os.listdir(files_dir)
    for file in files:
        data = read_data(f'{files_dir}\\{file}')
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


def fix_text(text):
    text = text.replace(',', ' ')
    return text.replace('\n', '')


def jsons_to_csv(files, output_name):
    with open(f'{output_name}.csv', 'w', newline='', encoding='utf-8') as f:
        wr = csv.writer(f)
        wr.writerow([
            'username',
            'user_link',
            'time',
            'text',
            'tags',
            'translated_text',
            'sentiment',
            'location',
            'lat_long',
            'lat',
            'long'
        ])
        for file in files:
            data = read_data(file)
            for d in data:
                lat, long = d['lat_long'].split(',')
                wr.writerow([
                    d['username'],
                    d['user-link'],
                    d['time'],
                    d['text'].replace(',', ' ').replace('\n', ' '),
                    ';'.join(d['tags']) if len(d['tags']) > 0 else 'none',
                    d['translated_text'].replace(',', ' ').replace('\n', ' '),
                    d['sentiment'],
                    d['location'],
                    d['lat_long'].replace(',', '_'),
                    lat,
                    long
                ])


def json_to_csv(file):
    with open(f'{file.replace(".json", ".csv")}', 'w', newline='', encoding='utf-8') as f:
        wr = csv.writer(f)
        wr.writerow([
            'username',
            'user_link',
            'time',
            'text',
            'tags',
            'translated_text',
            'sentiment',
            'location',
            'lat_long',
            'lat',
            'long'
        ])
        data = read_data(file)
        for d in data:
            lat, long = d['lat_long'].split(',')
            wr.writerow([
                d['username'],
                d['user-link'],
                d['time'].replace(',', '_'),
                d['text'].replace(',', '').replace('\n', ''),
                ';'.join(d['tags']) if len(d['tags']) > 0 else 'none',
                d['translated_text'].replace(',', '').replace('\n', ''),
                d['sentiment'],
                d['location'].replace(',', ''),
                d['lat_long'].replace(',', '_'),
                lat,
                long
            ])


if __name__ == '__main__':
    files = [
        'sentimental_analysis\\dummy_locations\\#corona_lebanon_tweets_11_7_2020.json',
        'sentimental_analysis\\dummy_locations\\#corona_tweets_12_7_2020.json',
        'sentimental_analysis\\dummy_locations\\healthcare_tweets_10_7_2020.json',
        'sentimental_analysis\\dummy_locations\\medical_tweets_11_7_2020.json'
    ]
    for file in files:
        json_to_csv(file)
    # jsons_to_csv(files, 'sentimental_analysis\\dummy_locations\\sentimental_analysis_tweets')
