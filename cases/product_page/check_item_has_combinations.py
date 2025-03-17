import unittest
import logging
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


from cases.tests.base_test import BaseTest
from pages.product_page import ProductPage
from pages.home_page import HomePage


class TestProductSelection(BaseTest):
    """Test case is:

    1. Open the product page
    2. Select color and size options
    3. Verify that the selections are successful
    """

    def test_select_product_options(self):
        """Verify that color and size selection is possible on the product page."""
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        self.logger.info("Navigating to the product page and checking for overlays...")

        home_page = HomePage(self.driver)
        home_page.ready()

        product_page = ProductPage(self.driver)

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

