from Scrapping import BeautifulSoupScrap as BSC
from Data.handle_data import save_json


def save(filename, css_selector):
    elements = BSC.get_elements(css_selector, source='https://sites.google.com/site/lebaneselanguage1/dictionary', attributes=True)
    res = []
    for e in elements:
        if e['text']:
            text = e['text'].strip().split('\n')
            if len(text) == 2:
                en, lb = text
                en = en.split('/')
                lb = lb.split('/')
                res.append({
                    'en': en,
                    'lb': lb
                })
    save_json(filename, res)


if __name__ == '__main__':
    css_selectors = "div#sites-canvas-main-content div > table:nth-child(2) > tbody > tr"
    save('English_Lebanese_Dictionary.json', css_selectors)
