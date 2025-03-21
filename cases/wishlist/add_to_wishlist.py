import unittest
import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from cases.tests.base_test import BaseTest
from pages.home_page import HomePage
from selenium.webdriver.support import expected_conditions as EC


class TestAddToWishlist(BaseTest):
    """Test case is:

    1. Search for a product
    2. Click on the favorite button of the first product
    3. Ensure the product is added to the wishlist
    """

    expected_search_keyword = "ayakkabı"


    def test_add_to_wishlist(self):
        """Searches for a product and adds it to the wishlist."""
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        time.sleep(2)
        self.logger.info(f"1. Searching for the product: {self.expected_search_keyword}")
        home_page = HomePage(self.driver)
        home_page.search_product(searchkey=self.expected_search_keyword)
        home_page.ready()
        self.logger.info("Search results are displayed.")

        self.logger.info("2. Scrolling down and clicking the favorite button on the first item")
        self.driver.execute_script("window.scrollBy(0, 100);")

        wait = WebDriverWait(self.driver, 10)
        add_to_wishlist = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "fvrt-btn")))
        add_to_wishlist.click()
        self.logger.info("Item successfully added to the wishlist.")

        home_page.ready()
