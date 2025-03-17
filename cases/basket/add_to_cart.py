import logging
import time
import unittest

from pages.cart_page import CartPage
from pages.home_page import HomePage
from pages.listing_page import ListingPage
from pages.product_page import ProductPage
from cases.tests.base_test import BaseTest


class TestAddToCart(BaseTest):
    """Test Case:

        1. Search for a product and open the product detail page.
        2. Select product options (color, size) and add it to the cart.
        3. Go to the cart and verify product details.
        4. Remove the product from the cart.
        """
    expected_search_keyword = "kazak"

    def test_add_to_cart(self):
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
        listing_page.open_dropdown()
        listing_page.selects_sort()

        self.logger.info("Clicking on the first product...")
        time.sleep(2)
        listing_page.clicks_first_product()
        home_page.ready()

        self.logger.info("Retrieving product details...")
        product_page = ProductPage(self.driver)
        home_page.ready()
        price = product_page.get_price()

        self.logger.info("Selecting product color...")
        color = product_page.select_color()
        self.assertIsNotNone(color, "Failed to select color!")

        self.logger.info("Selecting product size...")
        size = product_page.select_size()
        self.assertIsNotNone(size, "Failed to select size!")

        name = product_page.get_name()

        time.sleep(2)
        self.logger.info("Adding product to the cart...")
        product_page.add_to_basket()
        self.driver.implicitly_wait(5)

        self.logger.info("Navigating to the cart...")
        home_page.go_to_cart()
        home_page.ready()

        cart_page = CartPage(self.driver)
        time.sleep(1)
        self.logger.info("Retrieving cart item details...")
        cart_items = cart_page.cart_items()
        self.assertGreater(len(cart_items), 0, " No items found in the cart!")

        cart_names = " ".join(item.name for item in cart_items)
        self.assertIn(name, cart_names, f" {name} is not found in the cart!")

        cart_prices = (item.price for item in cart_items)
        total_price = sum(cart_prices)
        count = sum(item.count for item in cart_items)

        expected_total_price = float(price) * count
        if expected_total_price != total_price:
            self.logger.error(f"Price mismatch! Expected: {expected_total_price}, Found: {total_price}")
        self.assertEqual(expected_total_price, total_price)

        self.logger.info("Clearing the cart...")
        cart_page.cart_clear()
        time.sleep(2)

        self.logger.info("Test Passed: Product added, verified, and removed from the cart!")


if __name__ == "__main__":
    unittest.main()
