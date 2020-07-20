# from Scrapping import ChromeManager
# from twitter_config import CHROME_DRIVER
#
# if __name__ == '__main__':
#     cm = ChromeManager(driver_path=CHROME_DRIVER)
#     cm.close()

import twint

c = twint.Config()

# c.Username = "NBA"
c.Limit = 20
# c.Store_csv = True
# c.Output = "NBA"
c.Search = 'corona'
twint.run.Search(c)
