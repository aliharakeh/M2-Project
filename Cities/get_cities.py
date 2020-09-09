from Scrapping.beautiful_soup import BeautifulSoupScrap as BSC
import pandas as pd
import json
import time
import pyautogui
from Scrapping.chrome import ChromeManager

pyautogui.PAUSE = 1
pyautogui.FAILSAFE = True


def get_ar_cities():
    rows = BSC.get_elements('table tr', source='https://www.libandata.org/ar/mqal/layht-almdn-walqry-allbnanyt')
    data = []
    for row in rows[1:]:
        data.append([t.strip() for t in row.get_text().split('\n') if t])

    df = pd.DataFrame(data, columns=['Name', 'Kadaa', 'Mohafaza'])
    df.to_csv('cities_ar.csv', index=False)


def get_en_cities():
    rows = BSC.get_elements('table tr', source='https://www.libandata.org/en/article/list-cities-towns-and-villages-lebanon')
    data = []
    for row in rows[1:]:
        data.append([t.strip() for t in row.get_text().split('\n') if t])

    df = pd.DataFrame(data, columns=['Name', 'Kadaa', 'Mohafaza'])
    df.to_csv('cities_en.csv', index=False)


"""
##########################################################################################
"""

mo7afazat = {
    "Aakkar": '1',
    "عكار": '1',
    "Baalbek-Hermel": '2',
    "بعلبك-الهرمل": '2',
    "Beqaa": '4',
    "البقاع": '4',
    "Beyrouth": '3',
    "بيروت": '3',
    "Kesrouane Al Fatouh-Jbeil": '5',
    "كسروان الفتوح-جبيل": '5',
    "Liban-Nord": '7',
    "لبنان الشمالي": '7',
    "Liban-Sud": '8',
    "لبنان الجنوبي": '8',
    "Mont-Liban": '5',
    "جبل لبنان": '5',
    "Nabatiyeh": '6',
    "النبطية": '6'
}

kadaas = {
    "Aakkar": '11000',
    "عكار": '11000',
    "Aaley": '54000',
    "عاليه": '54000',
    "Baabda": '51000',
    "بعبدا": '51000',
    "Baalbek": '22000',
    "بعلبك": '22000',
    "Batroun": '74000',
    "البترون": '74000',
    "Bcharreh": '76000',
    "بشري": '76000',
    "Bent Jbeil": '62000',
    "بنت جبيل": '62000',
    "Beqaa Ouest": '42000',
    "البقاع الغربي": '42000',
    "Beyrouth": '31000',
    "بيروت": '31000',
    "Chouf": '53000',
    "الشوف": '53000',
    "Hasbaiya": '64000',
    "حاصبيا": '64000',
    "Hermel": '21000',
    "الهرمل": '21000',
    "Jbeil": '56000',
    "جبيل": '56000',
    "Jezzine": '82000',
    "جزين": '82000',
    "Kesrouane": '55000',
    "كسروان": '55000',
    "Koura": '72000',
    "الكورة": '72000',
    "Marjaayoun": '63000',
    "مرجعيون": '63000',
    "Matn": '52000',
    "المتن": '52000',
    "Minieh-Danniyeh": '77000',
    "المنية-الضنية": '77000',
    "Nabatiyeh": '61000',
    "النبطية": '61000',
    "Rachaiya": '43000',
    "راشيا": '43000',
    "Saida": '81000',
    "صيدا": '81000',
    "Sour": '83000',
    "صور": '83000',
    "Tripoli": '71000',
    "طرابلس": '71000',
    "Zahleh": '41000',
    "زحلة": '41000',
    "Zgharta": '73000',
    "زغرتا": '73000'
}

with open('mo7afazat.json', encoding='utf-8') as m:
    mo7afazat_data = json.loads(m.read())

with open('kaddaas.json', encoding='utf-8') as k:
    kadaas_data = json.loads(k.read())


def get_kadaa_info(k):
    id = kadaas[k]
    info = kadaas_data[id]
    return pd.Series([id, info['KADAA_AR'], info['KADAA_EN']])


def get_mo7afaza_info(m):
    id = mo7afazat[m]
    info = mo7afazat_data[id]
    return pd.Series([id, info['MOHAFAZA_AR'], info['MOHAFAZA_EN']])


def map_correct_mo7afazat_and_kadaas():
    df_ar = pd.read_csv('cities_ar.csv', header=0)
    df_en = pd.read_csv('cities_en.csv', header=0)

    df_ar[['KADAA_ID', 'KADAA_AR', 'KADAA_EN']] = df_ar.Kadaa.apply(get_kadaa_info)
    df_en[['KADAA_ID', 'KADAA_AR', 'KADAA_EN']] = df_en.Kadaa.apply(get_kadaa_info)

    df_ar[['MOHAFAZA_ID', 'MOHAFAZA_AR', 'MOHAFAZA_EN']] = df_ar.Mohafaza.apply(get_mo7afaza_info)
    df_en[['MOHAFAZA_ID', 'MOHAFAZA_AR', 'MOHAFAZA_EN']] = df_en.Mohafaza.apply(get_mo7afaza_info)

    df_ar.to_csv('cities_ar_v2.csv', index=False)
    df_en.to_csv('cities_en_v2.csv', index=False)


def get_lat_long():
    # use chrome driver to open google maps
    cm = ChromeManager(verbose=False)
    cm.load_page('https://www.google.com/maps')

    def scrape_lat_long(location):

        time.sleep(1.5)

        # automate the input in the search field the location name and run the search
        cm.set_value('input#searchboxinput', location)

        cm.click_element('#searchbox-searchbutton', delay_after_click=2)

        # automate the click on the + button to zoom the map
        cm.click_element('#widget-zoom-in')
        cm.click_element('#widget-zoom-in')
        cm.click_element('#widget-zoom-in')
        cm.click_element('#widget-zoom-in')
        cm.click_element('#widget-zoom-in')

        # automate the screen mouse click to put a marker on the map
        pyautogui.click(680, 530)

        time.sleep(0.5)

        # scrape the bottom pop-up window for lat,long values
        data = cm.get_value("div#reveal-card button.link-like.widget-reveal-card-lat-lng")
        location = cm.get_value("div#pane div.section-hero-header-title-description")
        try:
            lat, long = data.split(',')
            res = [location, lat, long.strip()]
        except:
            res = [None, -1, -1]

        print(res)
        return pd.Series(res)

    df_ar = pd.read_csv('cities_ar_v2.csv', header=0)
    df_en = pd.read_csv('cities_en_v2.csv', header=0)

    df_ar[['location', 'latitude', 'longitude']] = df_ar.Name.apply(scrape_lat_long)
    df_en[['location', 'latitude', 'longitude']] = df_en.Name.apply(scrape_lat_long)

    # close chrome
    cm.close()

    df_ar.to_csv('cities_ar_v3.csv', index=False)
    df_en.to_csv('cities_en_v3.csv', index=False)


if __name__ == '__main__':
    # get_ar_cities()
    # get_en_cities()
    # map_correct_mo7afazat_and_kadaas()
    get_lat_long()
