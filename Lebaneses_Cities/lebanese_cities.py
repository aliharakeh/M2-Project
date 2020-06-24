from Scrapping.beautiful_soup import BeautifulSoupScrap


def recursive_search(url, level=1):
    root_elements = BeautifulSoupScrap.get_elements(url, 'a')
    if len(root_elements) == 0:
        return

    for e in root_elements:
        a_elements = BeautifulSoupScrap.get_elements('', 'a')


if __name__ == '__main__':
    pass
