from Scrapping.beautiful_soup import BeautifulSoupScrap
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

    els = BeautifulSoupScrap.get_elements(link, 'a')[1:]
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
    els = BeautifulSoupScrap.get_elements(link, element)
    for e in els:
        print(e)


if __name__ == '__main__':
    search(link='http://www.fallingrain.com/world/LE/a')
    print(Lebanese_cities)

    with open('cities.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(Lebanese_cities, indent=2, ensure_ascii=False))


