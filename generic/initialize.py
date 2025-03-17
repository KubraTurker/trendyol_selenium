import threading
from dotenv import load_dotenv
import os
from selenium import webdriver
from selenium.common import TimeoutException, NoSuchWindowException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

assert os.getenv('USERNAME'), "USERNAME parameter needs to be present in the environment"


def accept_cookie(driver):
    wait = WebDriverWait(driver, 1000)
    wait.until(EC.visibility_of_element_located((By.ID, "onetrust-accept-btn-handler"))).click()


def watcher(driver):
    selectors = ['.overlay', '.onboarding .shadow']

    def check():
        while True:
            print('loop')
            try:
                for handle in driver.window_handles:
                    print(f"handle: {handle}")
                    driver.switch_to.window(handle)
                    print(f"window title: {driver.title}")
                    for selector in selectors:
                        try:
                            element = WebDriverWait(driver, 100).until(
                                EC.visibility_of_element_located((By.CSS_SELECTOR, selector))
                            )
                            print(element)
                            if element:
                                element.click()
                                print('Clicked popover button' + selector)
                        except TimeoutException:
                            print('no popover found')
            except NoSuchWindowException:
                print('no such window')




    w = threading.Thread(target=check, daemon=True)
    w.start()

    return w



def run() -> webdriver.Chrome:
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 1000)
    driver.get("https://www.trendyol.com/")
    driver.maximize_window()
    #watcher(driver)
    accept_cookie(driver)
    # page ready
    return driver
