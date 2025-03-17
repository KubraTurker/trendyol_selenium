import random
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class ListingPage:

    def __init__(self, driver):
        self.driver = driver
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

    def open_dropdown(self):
        """Opens the dropdown menu."""
        self.logger.info("Opening the dropdown...")
        wait = WebDriverWait(self.driver, 10)
        dropdown_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "select-w")))
        dropdown_button.click()
        self.logger.info("Dropdown opened successfully.")

    def get_sort(self):
        """Gets the available sorting options."""
        sorts = []
        wait = WebDriverWait(self.driver, 10)

        for element in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span.search-dropdown-text'))):
            sorts.append(element.text)

        self.logger.info(f"Available sorting options: {', '.join(sorts)}")
        return sorts

    def selects_sort(self):
        """Selects a random sort option."""
        sorts = self.get_sort()
        sort = random.choice(sorts)

        wait = WebDriverWait(self.driver, 10)
        sort_element = wait.until(EC.element_to_be_clickable(
            (By.XPATH, f'//span[contains(@class, "search-dropdown-text") and normalize-space(text())="{sort}"]')))
        sort_element.click()
        self.logger.info(f"Selected sort option: {sort}")
        return sort

    def clicks_first_product(self):
        """Clicks on the first product in the search results."""
        self.logger.info("🛒 Clicking on the first product in the search results...")
        wait = WebDriverWait(self.driver, 10)
        first_product = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.p-card-wrppr.with-campaign-view a')))
        first_product.click()
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.logger.info("First product clicked successfully.")