from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


class ChromeManager:
    _driver = None

    def __init__(self, driver_path='chromedriver', headless=False, window_size='1200x600'):
        _options = webdriver.ChromeOptions()
        _options.add_argument(f'window-size={window_size}')
        if headless:
            _options.add_argument('headless')
        self._driver = webdriver.Chrome(driver_path, options=_options)
        print('[INFO] Driver loaded...')

    def _wait_for_element(self, element_value, element_type, timeout):
        try:
            element_present = EC.presence_of_element_located((element_type, element_value))
            WebDriverWait(self._driver, timeout).until(element_present)
            print('[INFO] Page loaded')
            return True

        except TimeoutException:
            print('[INFO] Timed out waiting for page to load')
            return False

    def load_page(self, url, wait_element_value, wait_element_type=By.CSS_SELECTOR, wait_timeout=10):
        self._driver.get(url)
        return self._wait_for_element(wait_element_value, wait_element_type, wait_timeout)

    def get_elements(self, selector, single_element=False):
        elements = self._driver.find_elements_by_css_selector(selector)
        if single_element:
            return elements[0] if len(elements) == 1 else None
        return elements

    def click_element(self, selector, sleep_after_click=2):
        try:
            self._driver.find_element_by_css_selector(selector).click()
            print('[INFO] Click...')
            return 1

        except Exception as e:
            print(f'[ERROR]: {e}')
            return 0

        finally:
            if sleep_after_click:
                time.sleep(sleep_after_click)

    def scroll_page(self, scroll_count=10):
        # define initial page height for 'while' loop
        last_height = self._driver.execute_script("return document.body.scrollHeight")
        scrolls = 0

        while True:
            self._driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # define how many seconds to wait while dynamic page content loads
            time.sleep(3)

            # increment scroll count
            scrolls += 1

            # get new height
            new_height = self._driver.execute_script("return document.body.scrollHeight")

            # stop conditions
            if scrolls == scroll_count or new_height == last_height:
                break
            else:
                last_height = new_height

    def get_page_source(self):
        return self._driver.page_source
