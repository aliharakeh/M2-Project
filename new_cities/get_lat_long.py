from google_maps.HERE_maps import search_HERE_maps
import pandas as pd
import json


def get_lat_long(query):
    def _get_lat_long():
        res = search_HERE_maps(query)
        if res:
            lat, long, name, type_ = res[0]
            if 33 <= int(lat) <= 35 and 33 <= int(long) <= 35:
                res = [lat, long]
            else:
                res = [0, 0]
        else:
            res = [0, 0]
        return pd.Series(res)

    ar = pd.read_csv('cities_ar.csv', header=0)
    en = pd.read_csv('cities_en.csv', header=0)

    ar[['latitude', 'longitude']] = ar.Name.apply(_get_lat_long)
    en[['latitude', 'longitude']] = en.Name.apply(_get_lat_long)

    ar.to_csv('cities_ar_v2.csv')
    en.to_csv('cities_en_v2.csv')


def convert_to_json():
    ar = pd.read_csv('cities_ar_v2.csv', header=0)
    en = pd.read_csv('cities_en_v2.csv', header=0)

    res = []
    for i, row in ar.iterrows():
        if row['latitude'] != 0:
            name = row['Name']
            del row['Name']
            res.append({
                **row,
                'name': name,
                'latin': [],
                'non-latin': [name],
            })

    for i, row in en.iterrows():
        if row['latitude'] != 0:
            name = row['Name']
            del row['Name']
            res.append({
                **row,
                'name': name,
                'latin': [name],
                'non-latin': [],
            })

    with open('cities_details.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(res, indent=2, ensure_ascii=False))


def join():
    ar = pd.read_csv('cities_ar_v2.csv', header=0)
    en = pd.read_csv('cities_en_v2.csv', header=0)

    ar = ar[ar.latitude == 0]
    en = en[en.latitude == 0]

    # columns = ["KADAA_ID", "KADAA_AR", "KADAA_EN", "MOHAFAZA_ID", "MOHAFAZA_AR", "MOHAFAZA_EN", "latitude", "longitude"]
    # res = pd.merge(ar, en, how='inner', left_on=columns, right_on=columns)
    print(ar.count())
    print(en.count())
    # print(res.count())
    # print(res.loc[0])


if __name__ == '__main__':
    # get_lat_long()
    # convert_to_json()
    join()

    # count
    # with open('cities_details.json', encoding='utf-8') as f: \
    #     print(len(json.loads(f.read())))
