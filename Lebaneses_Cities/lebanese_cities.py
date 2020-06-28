from Scrapping.beautiful_soup import BeautifulSoupScrap as BSC
import re
import json

Lebanese_cities = {}
COUNT = 0


def create_key_tree(key_list):
    global Lebanese_cities
    refrence = Lebanese_cities
    for key in key_list:
        if key not in refrence:
            refrence[key] = {}
        refrence = refrence[key]


def search(link, link_text=None, parent_link=None, levels=None, root=True):
    global Lebanese_cities, COUNT

    # if COUNT == 20:
    #     return

    # print('------------------------')
    if not levels:
        levels = []

    leaf_link = re.search(r'/LE/\d+', link)
    if leaf_link or 'world' not in link:
        # print(f'[Parent Link]: {parent_link}')
        # levels.append('cities')
        # print(f'[Levels]: {levels}')
        # print(f'[Children Leaf Link]: {link}')
        ref = Lebanese_cities
        for level in levels:
            ref = ref[level]
        if 'cities' not in ref:
            ref['cities'] = []
        ref['cities'].append(link)
        # print(ref['cities'])
        return

    els = BSC.get_elements_from_url(link, 'a')[1:]
    if not root:
        levels.append(link_text)
        create_key_tree(levels)
        COUNT += 1

    # print(f'[Link]: {link}')
    # print(f'[Parent Link]: {parent_link}')
    print(f'[Levels]: {levels}')
    # print(f'[Children Links]: {len(els)}')

    for e in els:
        search('http://www.fallingrain.com' + e['href'], e['text'], link, levels[:], False)


def check(link, element):
    els = BSC.get_elements_from_url(link, element)
    for e in els:
        print(e)


def save(filename, data):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(json.dumps(data, indent=2, ensure_ascii=False))


def get_cities_count(cities_json):
    def add_cities_count(key, d: dict):
        if key in d:
            d['cities_count'] = len(d[key])
            return

        for k in d.keys():
            add_cities_count(key, d[k])

    with open(cities_json, 'r', encoding='utf-8') as f:
        data = json.loads(f.read())

    add_cities_count('cities', data)

    return data


def get_all_links(cities_2_json):
    links = {}

    def get_cities_links(key, d: dict, links):
        if key in d:
            links += d[key]
            return

        for k in d.keys():
            get_cities_links(key, d[k], links)

    with open(cities_2_json, 'r', encoding='utf-8') as f:
        data = json.loads(f.read())

    get_cities_links('cities', data, links)

    return links


def get_cities_info(cities_3_json):
    cities = {}

    def get_element_text(bs4, selector):
        e = BSC.get_elements_from_bs4(bs4, selector, single_element=True)
        return e['text'] if e else None

    def get_city_info(url):
        bs4 = BSC.get_bs4_from_url(url)
        name = get_element_text(bs4, 'h1')
        h3s = BSC.get_elements_from_bs4(bs4, 'h3')
        latitude = get_element_text(bs4, 'tr:nth-child(1) > td:nth-child(2)')
        lat_dms = get_element_text(bs4, 'tr:nth-child(2) > td:nth-child(2)')
        longitude = get_element_text(bs4, 'tr:nth-child(1) > td:nth-child(4)')
        long_dms = get_element_text(bs4, 'tr:nth-child(2) > td:nth-child(4)')
        altitude_feet = get_element_text(bs4, 'tr:nth-child(1) > td:nth-child(6)')
        altitude_meters = get_element_text(bs4, 'tr:nth-child(2) > td:nth-child(6)')
        population = get_element_text(bs4, 'tr:nth-child(4) > td')
        return {
            'name': name.split(',')[0] if name else None,
            'latin': h3s[0]['text'][21:].split(',') if len(h3s) > 0 else None,
            'non-latin': h3s[1]['text'][25:].split(',') if len(h3s) > 1 else None,
            'latitude': latitude if latitude else None,
            'longitude': longitude if longitude else None,
            'lat(DMS)': lat_dms if lat_dms else None,
            'long(DMS)': long_dms if long_dms else None,
            'altitude(feet)': altitude_feet if altitude_feet else None,
            'altitude(meters)': altitude_meters if altitude_meters else None,
            'population': population if population else None,
        }

    # def cities_info(d: dict, cities):
    #     if 'cities' in d:
    #         for city_url in d['cities']:
    #             cities[f'{len(cities)}_{city_url}'] = get_city_info(city_url)
    #         return
    #
    #     for k in d.keys():
    #         cities_info(d[k], cities)

    with open(cities_3_json, 'r', encoding='utf-8') as f:
        data = json.loads(f.read())

    total = len(data)

    # cities_info(data, cities)
    for index, city_url in enumerate(data):
        key = f'{index + 1}_{city_url}'

        if index % 10 == 0:
            print(f'{index} / {total}')

        if key in cities:
            continue

        cities[key] = get_city_info(city_url)

    return cities


def get_cities_2_levels_dict(cities_4_json):
    english_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                       't', 'u', 'v', 'w', 'x', 'y', 'z']
    arabic_letters = ['ا', 'ب', 'ت', 'ث', 'ج', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'س', 'ش', 'ص', 'ض', 'ط', 'ظ', 'ع', 'غ',
                      'ف', 'ق', 'ك', 'ل', 'م', 'ن', 'ه', 'و', 'ي', 'ء']
    cities = {}

    def create_dictionary_items(letter, dictionary, english=True):
        letters = english_letters
        if not english:
            letters = arabic_letters
        dictionary[letter] = {l: [] for l in letters}

    def fill_cities(letters, dictionary, english=True):
        for l in letters:
            create_dictionary_items(l, dictionary, english=english)

    def get_city_list(data):
        city_list = []
        if data['name']:
            city_list.append(data['name'])
        if data['latin']:
            city_list += data['latin']
        if data['non-latin']:
            city_list += data['non-latin']
        return city_list

    fill_cities(english_letters, cities)
    fill_cities(arabic_letters, cities, english=False)

    with open(cities_4_json, 'r', encoding='utf-8') as f:
        data = json.loads(f.read())

    for key, value in data.items():
        city_list = get_city_list(value)
        for c in city_list:
            if not c or len(c) < 2:
                continue
            c1 = c.lower()
            k1 = c1[0]
            k2 = c1[1]
            if k1 not in cities:
                cities[k1] = {}
            if k2 not in cities[k1]:
                cities[k1][k2] = []
            cities[k1][k2].append(c)

    # clean result
    cities_final = {}
    for k1, v1 in cities.items():
        cities_final[k1] = {}
        for k2, v2 in v1.items():
            if len(v2) > 0:
                cities_final[k1][k2] = list({v for v in v2})

    return cities_final


def get_all_cities(cities_4_json):
    cities = {}

    def get_city_list(data):
        city_list = []
        if data['name']:
            city_list.append(data['name'])
        if data['latin']:
            city_list += data['latin']
        if data['non-latin']:
            city_list += data['non-latin']
        return city_list

    with open(cities_4_json, 'r', encoding='utf-8') as f:
        data = json.loads(f.read())

    for key, value in data.items():
        city_list = get_city_list(value)
        for c in city_list:
            if not c:
                continue
            cities[c] = value

    return cities


if __name__ == '__main__':
    # search(link='http://www.fallingrain.com/world/LE/a')
    # print(Lebanese_cities)
    # save('cities.json', Lebanese_cities)

    # data = get_cities_count('cities.json')
    # save('cities_2.json', data)

    # data = get_all_links('cities_2.json')
    # save('cities_3.json', data)

    # data = get_cities_info('cities_3.json')
    # save('cities_4.json', data)

    # TODO: clean arabic letters
    # data = get_cities_2_levels_dict('cities_4.json')
    # save('cities_5.json', data)

    data = get_all_cities('cities_4.json')
    save('cities_6.json', data)
