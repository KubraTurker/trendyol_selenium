import random
import logging
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

class ProductPage:

    def __init__(self, driver):
        self.driver = driver
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

    def get_name(self):
        """
        Gets the name of the product.
        """

        name = self.driver.find_element(By.CLASS_NAME, 'pr-new-br').text
        self.logger.info(f"Product name: {name}")

        return name

    def get_price(self):
        """
        Gets the price of the product.
        """

        wait = WebDriverWait(self.driver, 10)
        try:
            price_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'campaign-price')))
        except:
            try:
                price_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'prc-dsc')))
            except:
                self.logger.error("Price information not found!")
                raise ValueError("Price information not found!")

        price = price_element.text.strip()

        price = price.replace(" TL", "").replace(" ", "").replace(".", "").replace(",", ".")

        try:
            price_float = float(price)
            self.logger.info(f"Product price: {price_float}")

            return price_float

        except ValueError:
            self.logger.error(f"Invalid price format: {price}")
            raise ValueError(f"Invalid price format: {price}")

    def get_colors(self):
        """Gets the available colors for the product."""
        colors = []
        for color_name in self.driver.find_elements(By.CLASS_NAME, 'slc-img'):
            colors.append(color_name.get_attribute('title'))

        self.logger.info(f"Available colors: {', '.join(colors)}")
        return colors

    def select_color(self):
        """
        Selects a random color for the product.
        """

        try:
            colors = self.get_colors()
            if not colors:
                self.logger.info("No color options available for this product.")
                return None

            color = random.choice(colors)
            wait = WebDriverWait(self.driver, 10)
            color_element = wait.until(EC.visibility_of_element_located((By.XPATH,
                                                                   f'//a[contains(@class, "slc-img") and @title="{color}"]')))
            color_element.click()
            self.logger.info(f"Color '{color}' selected successfully!")
            return color

        except Exception as e:
            self.logger.error(f"Error in selecting color: {e}")
            print("Error:", e)

    def get_sizes(self):
        """
        Gets the available sizes for the product.
        """

        sizes = []

        for size_element in self.driver.find_elements(By.XPATH, f'//div[contains(@class, "sp-itm") and not(contains(@class, "so"))]'):
            sizes.append(size_element.text)

        self.logger.info(f"Available sizes: {', '.join(sizes)}")

        return sizes

    def select_size(self):
        """
        Selects a random size for the product.
        """

        try:
            sizes = self.get_sizes()
            size = random.choice(sizes)
            wait = WebDriverWait(self.driver, 10)
            size_element = wait.until(
                EC.element_to_be_clickable((By.XPATH, f'//div[contains(@class, "sp-itm") and normalize-space(text())="{size}"]')))

            size_element.click()
            self.logger.info(f"Size '{size}' selected successfully!")

            return size

        except Exception as e:
            self.logger.error(f"Error in selecting size: {e}")
            print("Error:", e)

    def add_to_basket(self):
        """
        Adds the product to the basket.
        """

        try:
            wait = WebDriverWait(self.driver, 10)
            add_to_basket = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'add-to-basket')))
            add_to_basket.click()
            self.logger.info("Product added to the basket successfully.")

        except Exception as e:
            self.logger.error(f"Error while adding the product to the basket: {e}")
            print(f"Error while adding the product to the basket: {e}")
            raise e
