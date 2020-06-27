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


def get_cities_count(json_file):
    def add_cities_count(key, d: dict):
        if key in d:
            d['cities_count'] = len(d[key])
            return

        for k in d.keys():
            add_cities_count(key, d[k])

    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.loads(f.read())

    add_cities_count('cities', data)

    return data


def get_all_links(json_file):
    links = {}

    def get_cities_links(key, d: dict, links):
        if key in d:
            links += d[key]
            return

        for k in d.keys():
            get_cities_links(key, d[k], links)

    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.loads(f.read())

    get_cities_links('cities', data, links)

    return links


def get_cities_info(json_file):
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

    with open(json_file, 'r', encoding='utf-8') as f:
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


if __name__ == '__main__':
    # search(link='http://www.fallingrain.com/world/LE/a')
    # print(Lebanese_cities)
    # save('cities.json', Lebanese_cities)

    # data = get_cities_count('cities.json')
    # save('cities_2.json', data)

    # data = get_all_links('cities_2.json')
    # save('cities_3.json', data)

    # check('http://www.fallingrain.com/world/LE/07/Beit_Yahoun.html', "tr:nth-child(4) > td")

    data = get_cities_info('cities_3.json')
    save('cities_4.json', data)

    # e = BSC.get_elements_from_url('http://www.fallingrain.com/world/LE/07/Beit_Yahoun.html', 'h6')
    # print(e)