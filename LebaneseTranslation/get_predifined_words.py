from Scrapping import BeautifulSoupScrap as BSC
from Data.handle_data import save_json
import csv


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


def save_csv():
    with open('lb_en.txt', 'r') as f:
        lines = f.read().split('\n')

    with open('lb_en.csv', 'w', newline='', encoding='utf-8') as f:
        wr = csv.writer(f)
        wr.writerow(['Lebanese', 'English'])
        for line in lines:
            lb, en = line.strip().split('\t')
            rows = lb.split('/')
            for r in rows:
                wr.writerow([r, en])


def verbs():
    with open('verbs.txt', 'r') as v:
        data = v.read().split('___')[1:]
    res = set()
    for d in data:
        lines = d.split('\n')
        meaning = None
        for i, line in enumerate(lines):
            if i == 0:
                meaning = line.replace('(to)', '').strip()
            else:
                split = line.split('/')
                for s in split:
                    res.add(f'{s},{meaning}')
    return list(res)


if __name__ == '__main__':
    # css_selectors = "div#sites-canvas-main-content div > table:nth-child(2) > tbody > tr"
    # save('English_Lebanese_Dictionary.json', css_selectors)
    # save_csv()
    save_json('verbs.json', verbs())