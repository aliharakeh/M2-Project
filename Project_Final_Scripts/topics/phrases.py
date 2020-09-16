from Text_Mining.text_processing import TextProcessing
import pandas as pd
import json

needed_months_data = ['08', '09']


def get_grams(tp, n_range, limit):
    ngrams = []
    for n in n_range:
        series = tp.most_frequent_n_grams(n=n, limit=limit)
        ngrams += list(series.index)
    return ngrams


def pre_processing(df, stop_words):
    tp = TextProcessing(df, 'text')
    tp.pre_process.remove_non_alphabet()
    tp.pre_process.to_lower_case()
    if stop_words:
        tp.pre_process.remove_stop_words(stop_words)
    return tp


def get_phrases(df, groupby, save_to, ngrams, limit):
    groups = df.groupby(groupby)
    data_dict = {}
    for g_k, g_data in groups:
        id_, ar, en, m = g_k
        if m in needed_months_data:
            tp = pre_processing(g_data.copy(), None)
            data_dict["_".join([str(id_), ar, en, m])] = get_grams(tp, ngrams, limit)

    with open(save_to, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data_dict, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    df = pd.read_csv('..\\tweets_data.csv')
    df[['year', 'month', 'day']] = df.date.str.split('-', expand=True)

    kadaas_groupby = ['KADAA_ID', 'KADAA_AR', 'KADAA_EN', 'month']
    mo7afazat_groupby = ['MOHAFAZA_ID', 'MOHAFAZA_AR', 'MOHAFAZA_EN', 'month']

    get_phrases(df, kadaas_groupby, 'kadaas_phrases.json', (2, 3), 25)
    get_phrases(df, mo7afazat_groupby, 'mo7afazat_phrases.json', (2, 3), 25)

    print('Done!!')
