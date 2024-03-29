import time

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

from selenium_toolkit import SeleniumToolKit


def test_webdriver_is_open():
    options = Options()
    options.add_argument('--start-maximized')
    driver = Chrome(options=options)

    sk = SeleniumToolKit(driver=driver)

    sk.goto('https://webscraper.io/test-sites/e-commerce/allinone/product/545')

    time.sleep(2)
    driver.close()

    assert not sk.webdriver_is_open()
