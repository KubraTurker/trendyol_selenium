import unittest
import logging
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from generic import initialize, auth


class TestUserLoginValidation(unittest.TestCase):
    """Test case is:

    1. Open the browser and navigate to the login page
    2. Test login scenarios: empty email, empty password, wrong password
    3. Verify the error messages displayed
    """

    def setUp(self):
        """Initialize the browser and navigate to login page."""
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        self.logger.info("Initializing browser and navigating to the login page...")
        self.driver = initialize.run()
        auth.go_login(self.driver)

    def close_popup(self):
        """Close any pop-up if present."""
        wait = WebDriverWait(self.driver, 10)
        try:
            element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'i-cancel')))
            element.click()
            self.logger.info("Pop-up closed successfully.")
        except:
            self.logger.info("No pop-up to close.")

    def login_button(self):
        """Click on the login button."""
        wait = WebDriverWait(self.driver, 10)
        login_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='login-register']/div[3]/div[1]/form/button"))
        )
        login_button.click()
        self.logger.info("Login button clicked.")

    def error_message(self):
        """Check for the error message and log its text."""
        try:
            error_message = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "span.message"))
            )
            self.logger.warning(f"Error message displayed: {error_message.text}")
        except Exception as e:
            self.logger.error(f"No error message found or failed to load: {e}")

    def login_email(self):
        """Enter an email into the email field."""
        wait = WebDriverWait(self.driver, 10)
        login_email = wait.until(EC.element_to_be_clickable((By.ID, "login-email")))
        login_email.send_keys("x@gmail.com")
        self.logger.info("Email entered successfully.")

    def login_password(self):
        """Enter a password into the password field."""
        wait = WebDriverWait(self.driver, 10)
        login_password = wait.until(EC.element_to_be_clickable((By.ID, "login-password-input")))
        login_password.send_keys("12345")
        self.logger.info("Password entered successfully.")

    def test_empty_email(self):
        """Test login attempt with empty email."""
        self.logger.info("Testing login with empty email...")
        time.sleep(3)
        self.close_popup()
        self.login_button()
        self.error_message()

    def test_empty_password(self):
        """Test login attempt with empty password."""
        self.logger.info("Testing login with empty password...")
        self.login_email()
        self.login_button()
        self.error_message()

    def test_wrong_password(self):
        """Test login attempt with incorrect password."""
        self.logger.info("Testing login with incorrect password...")
        self.login_password()
        self.login_button()
        self.error_message()
        time.sleep(2)

    def tearDown(self):
        """Close the browser."""
        self.logger.info("Closing the browser and ending the test.")
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
