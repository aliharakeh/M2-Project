import json
import pandas


def json_to_csv(dict_, type_, filename):
    data = []
    for key, topics in dict_.items():
        data.append([*key.split('_'), topics])
    df = pandas.DataFrame(data, columns=['year', 'month', f'{type_}_ID', f'{type_}_AR', f'{type_}_EN', 'Topics'])
    df.to_csv(filename, index=False)


if __name__ == '__main__':
    with open('mo7afazat_topics_old.json', encoding='utf-8') as f:
        mo7afazat = json.loads(f.read())

    with open('kadaas_topics_old.json', encoding='utf-8') as f:
        kadaas = json.loads(f.read())

    json_to_csv(mo7afazat, 'MOHAFAZA', 'mo7afazat_topics')
    json_to_csv(kadaas, 'KADAA', 'kadaas_topics')
