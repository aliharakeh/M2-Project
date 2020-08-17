from Text_Mining.text_processing import TextProcessing
import pandas as pd
import json


def get_grams(tp, n_range, limit):
    ngrams = []
    for n in n_range:
        series = tp.most_frequent_n_grams(n=n, limit=limit)
        res = {}
        for index, value in series.items():
            res[str(index)] = int(value)
        ngrams.append(res)
    return ngrams


def pre_processing(df, stop_words):
    tp = TextProcessing(df, 'text')  # translated_text
    tp.pre_process.remove_non_alphabet()
    if stop_words:
        tp.pre_process.remove_stop_words(stop_words)
    return tp


def location_phrases(df, stop_words):
    locations = df['location'].unique()
    loc_dict = {}
    for location in locations:
        temp_df = (df[df['location'] == location]).copy()
        tp = pre_processing(temp_df, stop_words)
        loc_dict[location] = get_grams(tp, [2, 3, 4, 5], 50)

    with open('locations_phrases.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(loc_dict, indent=2, ensure_ascii=False))


def kaddaas_phrases(df, stop_words):
    kadaas = df['KADAA_ID'].unique()
    kaddaa_dict = {}
    for kaddaa in kadaas:
        temp_df = (df[df['KADAA_ID'] == kaddaa]).copy()
        tp = pre_processing(temp_df, stop_words)
        kaddaa_dict[int(kaddaa)] = get_grams(tp, [2, 3, 4, 5], 50)

    with open('kaddaas_phrases.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(kaddaa_dict, indent=2, ensure_ascii=False))


def mo7afazat_phrases(df, stop_words):
    mohafazat = df['MOHAFAZA_ID'].unique()
    mohafaza_dict = {}
    for mohafaza in mohafazat:
        temp_df = (df[df['MOHAFAZA_ID'] == mohafaza]).copy()
        tp = pre_processing(temp_df, stop_words)
        mohafaza_dict[int(mohafaza)] = get_grams(tp, [2, 3, 4, 5], 50)

    with open('mo7afazat_phrases.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(mohafaza_dict, indent=2, ensure_ascii=False))


def mo7afazat(df):
    grp = df.groupby(['MOHAFAZA_ID', 'MOHAFAZA_AR', 'MOHAFAZA_EN'])
    res = {}
    for name, group in grp:
        res[int(name[0])] = {
            'MOHAFAZA_AR': name[1],
            'MOHAFAZA_EN': name[2]
        }
    with open('mo7afazat.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(res, indent=2, ensure_ascii=False))


def kaddaas(df):
    grp = df.groupby(['KADAA_ID', 'KADAA_AR', 'KADAA_EN'])
    res = {}
    for name, group in grp:
        res[int(name[0])] = {
            'KADAA_AR': name[1],
            'KADAA_EN': name[2]
        }
    with open('kaddaas.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(res, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    df = pd.read_csv('all.csv')
    mo7afazat_phrases(df, None)
    kaddaas_phrases(df, None)

    # mo7afazat(df)
    # kaddaas(df)
