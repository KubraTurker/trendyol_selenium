from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.ie.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
from time import sleep


class ProductPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def get_name(self):
        name = self.driver.find_element(By.CLASS_NAME, 'pr-new-br').text

        return name

    def get_price(self) -> float:
        price = self.driver.find_element(By.CLASS_NAME, 'prc-dsc').text
        price = price.replace(" TL", "").replace(",", ".").replace(" ", "")
        try:
            return float(price)
        except ValueError:
            raise ValueError(f"Geçersiz fiyat formatı: {price}")

    def select_size(self):
        try:
            sizes = self.get_sizes()
            size = random.choice(sizes)
            wait = WebDriverWait(self.driver, 1)
            size_element = wait.until(EC.element_to_be_clickable((By.XPATH,f'//div[@class="sp-itm" and normalize-space(text())="{size}"]')))

            size_element.click()
            print(f"Size '{size}' selected successfully!")
            return size
        except Exception as e:
            print("Error:", e)

    def select_color(self):
        try:
            colors = self.get_colors()
            color = random.choice(colors)
            wait = WebDriverWait(self.driver, 1)
            color_element = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                         f'//a[contains(@class, "slc-img") and @title="{color}"]')))
            color_element.click()
            print(f"Color '{color}' selected successfully!")
            return color
        except Exception as e:
                print("Error:", e)



    def add_to_basket(self):
        try:
            wait = WebDriverWait(self.driver, 1)
            add_basket = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'add-to-basket')))
            add_basket.click()
        except Exception as e:
            print(f"Ürünü sepete eklerken hata oluştu: {e}")
            raise e

    def get_sizes(self):
        sizes = []

        for size_element in self.driver.find_elements(By.CLASS_NAME, 'sp-itm'):
            sizes.append(size_element.text)

        return sizes

    def get_colors(self):
        colors = []

        for color_name in self.driver.find_elements(By.CLASS_NAME, 'slc-img'):
            colors.append(color_name.get_attribute('title'))

        return colors

