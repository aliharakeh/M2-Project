from .chrome import ChromeManager
from twitter_config import CHROME_DRIVER


class LebanonCitiesScrapper:
    def __init__(self, chrome_manager):
        # instance variables
        self._cm: ChromeManager = chrome_manager


if __name__ == '__main__':
    cm = ChromeManager(driver_path=CHROME_DRIVER)
    lb_cities = LebanonCitiesScrapper(cm)
