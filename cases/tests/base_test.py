import unittest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options

from generic import auth
from pages.home_page import HomePage


class BaseTest(unittest.TestCase):
    base_url = "https://www.trendyol.com/"

    def setUp(self):
        options = Options()
        options.add_argument("start-maximized")
        options.add_argument("disable-popup-blocking")
        options.add_argument("disable-extensions")
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(self.base_url)
        self.driver.implicitly_wait(10)
        self.wait = WebDriverWait(self.driver, 10)
        home_page = HomePage(self.driver)
        home_page.accept_cookie()
        auth.run(self.driver)

    def tearDown(self):
        self.driver.quit()