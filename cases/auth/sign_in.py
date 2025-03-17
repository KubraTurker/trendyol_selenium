# Kullanici login olabiliyor mu kontrolu yapilir
# 1. Ana sayfaya gidilir
# 2. Login Butonuna tiklanir
# 3. Bilgiler girilir
# 4. Hesabim butonuna tiklanir
# 5. Hesabim sayfasinin acildigi dogrulanir
import unittest
import logging
import time

from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from cases.tests.base_test import BaseTest

class TestUserLogin(BaseTest):
    """Test case is:

    1. Open the browser and log in to the system
    2. Click the account login button
    3. Verify that the 'My Account' page is displayed
    """

    def click_stable_element(self, by, value, retries=3):
        """Click on an element safely, retrying if it becomes stale."""
        for attempt in range(retries):
            try:
                element = self.driver.find_element(by, value)
                element.click()
                self.logger.info(f"Element clicked successfully: {value}")
                return
            except (StaleElementReferenceException, NoSuchElementException):
                self.logger.warning(f"Attempt {attempt + 1}: Element not clickable yet, retrying...")
                time.sleep(1)

        self.logger.error(f"Failed to click element after {retries} attempts: {value}")
        raise Exception(f"Element {retries} attempts failed to click!")

    def test_user_can_login(self):
        """Verify that the user can log in and see the 'My Account' page."""
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        self.logger.info("1. Clicking on the account login button...")
        self.click_stable_element(By.CSS_SELECTOR, ".account-nav-item.user-login-container")

        self.logger.info("2. Waiting for the 'My Account' page to load...")
        wait = WebDriverWait(self.driver, 10)
        try:
            account_page_check = wait.until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'section-user_info'))
            )
            self.assertTrue(account_page_check.is_displayed(), "'My Account' page did not open!")
            self.logger.info("'My Account' page successfully loaded.")
        except TimeoutException:
            self.logger.error("'My Account' page did not load within the expected time!")
            self.fail("'My Account' page did not open in time!")


if __name__ == "__main__":
    unittest.main()
