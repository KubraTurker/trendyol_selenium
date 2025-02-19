from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

def go_login(driver):
    wait = WebDriverWait(driver, 1000)
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "user-login-container"))).click()


def login(driver):
    wait = WebDriverWait(driver, 1000)
    wait.until(EC.element_to_be_clickable((By.ID, "login-email"))).send_keys(os.getenv("USERNAME"))
    wait.until(EC.element_to_be_clickable((By.ID, "login-password-input"))).send_keys(os.getenv("PASSWORD"))
    wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='login-register']/div[3]/div[1]/form/button"))).click()


def run (driver):
    go_login(driver)
    login(driver)