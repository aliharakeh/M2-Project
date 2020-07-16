from Scrapping import ChromeManager
from twitter_config import CHROME_DRIVER

if __name__ == '__main__':
    cm = ChromeManager(driver_path=CHROME_DRIVER)
    cm.close()