from bs4 import BeautifulSoup
import requests
import json


class BeautifulSoupScrap:

    @staticmethod
    def get_page_source(url):
        return requests.get(url).content

    @staticmethod
    def get_bs4(html):
        return BeautifulSoup(html, 'html.parser')

    @staticmethod
    def get_elements(page_url, element_css_selector):
        html = BeautifulSoupScrap.get_page_source(page_url)
        bs4 = BeautifulSoupScrap.get_bs4(html)
        elements = bs4.select(element_css_selector)
        data = []
        for e in elements:
            data.append({
                **e.attrs,  # all tag attributes
                'text': e.get_text()
            })
        return data

    @staticmethod
    def save_as_json(filename, elements_list):
        with open(f'{filename}.json', 'w', encoding='utf8') as file:
            file.write(json.dumps(elements_list, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    els = BeautifulSoupScrap.get_elements('http://www.fallingrain.com/world/LE/', 'a')
    BeautifulSoupScrap.save_as_json('bs4_test', els)
    for el in els:
        print(el)
        print('-----------------------------------')
