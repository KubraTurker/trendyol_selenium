import unittest
import logging
import time

from cases.tests.base_test import BaseTest
from pages.product_page import ProductPage
from pages.home_page import HomePage
from pages.listing_page import ListingPage


class TestProductSelection(BaseTest):
    """Test case is:

    1. Open the product page
    2. Select color and size options
    3. Verify that the selections are successful
    """
    expected_search_keyword = "kazak"

    def test_select_product_options(self):
        """Verify that color and size selection is possible on the product page."""
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        time.sleep(2)
        self.logger.info(f"Searching for a product: {self.expected_search_keyword}")
        home_page = HomePage(self.driver)
        home_page.search_product(searchkey=self.expected_search_keyword)
        home_page.ready()

        self.logger.info("Selecting a random sorting option...")
        listing_page = ListingPage(self.driver)
        home_page.ready()

        self.logger.info("Clicking on the first product...")
        time.sleep(2)
        listing_page.clicks_first_product()
        home_page.ready()

        product_page = ProductPage(self.driver)
        home_page.ready()

        self.logger.info("Selecting color option...")
        color = product_page.select_color()
        self.assertIsNotNone(color, "Color selection failed!")
        self.logger.info("Color selection successful!")

        self.logger.info("Selecting size option...")
        size = product_page.select_size()
        self.assertIsNotNone(size, "Size selection failed!")
        self.logger.info("Size selection successful!")

        self.logger.info("Product options have been successfully selected.")


if __name__ == "__main__":
    unittest.main()

