import time
import logging

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait



class HomePage:
    def __init__(self, driver):
        self.driver = driver
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)


    def search_product(self, searchkey):
        """
        Search for a product
        """

        self.logger.info(f"🔍 Searching for '{searchkey}'...")
        wait = WebDriverWait(self.driver, 10)
        search = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@data-testid = "suggestion"]')))
        search.send_keys(searchkey)
        search.send_keys(Keys.ENTER)
        time.sleep(2)
        self.logger.info(f"Search for '{searchkey}' completed successfully!")

    def go_to_cart(self):
        """
        Navigate to the cart
        """

        self.logger.info("🛒 Navigating to the cart...")
        wait = WebDriverWait(self.driver, 10)
        go_to_basket = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '.account-nav-item.basket-preview'))
        )
        go_to_basket.click()
        self.logger.info("Successfully navigated to the cart.")

    def ready(self):
        """
        Handle pop-ups if necessary
        """

        try:
            wait = WebDriverWait(self.driver, 10)
            element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
            element.click()
            self.logger.info("Pop-up closed successfully.")
        except:
            self.logger.info("No pop-up found, continuing.")

    def scroll(self):
        """
        it scrolls down on the page (0,250)
        """

        self.driver.execute_script("window.scrollBy(0, 100);")

    def accept_cookie(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.visibility_of_element_located((By.ID, "onetrust-accept-btn-handler"))).click()
