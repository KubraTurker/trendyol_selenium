import random
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

class ProductPage:
    def __init__(self, driver):
        self.driver = driver

    def get_name(self):
        """Ürünün ismini alır"""
        name = self.driver.find_element(By.CLASS_NAME, 'pr-new-br').text
        return name

    def get_price(self):
        """Ürünün fiyatını alır"""
        try:

            price_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'campaign-price')))
        except:
            try:
                # Eğer kampanyalı fiyat yoksa, normal fiyatı al
                price_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'prc-dsc')))
            except:
                raise ValueError("Fiyat bilgisi bulunamadı!")

        price = price_element.text.strip()

        if not price:
            raise ValueError("Fiyat boş geldi! Sayfa yüklenmemiş olabilir veya element yanlış.")

        price = price.replace(" TL", "").replace(" ", "").replace(".", "").replace(",", ".")

        try:
            return float(price)
        except ValueError:
            raise ValueError(f"Geçersiz fiyat formatı: {price}")


    def get_colors(self):
        colors = []

        for color_name in self.driver.find_elements(By.CLASS_NAME, 'slc-img'):
            colors.append(color_name.get_attribute('title'))

        return colors

    def select_color(self):
        """Ürün için renk seçimi yapar"""
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

    def get_sizes(self):
        sizes = []

        for size_element in self.driver.find_elements(By.XPATH, f'//div[contains(@class, "sp-itm") and not(contains(@class, "so"))]'):
            sizes.append(size_element.text)

        return sizes

    def select_size(self):
        """Ürün için beden seçimi yapar"""
        try:
            sizes = self.get_sizes()
            size = random.choice(sizes)
            wait = WebDriverWait(self.driver, 10)
            size_element = wait.until(
                EC.element_to_be_clickable((By.XPATH, f'//div[contains(@class, "sp-itm") and normalize-space(text())="{size}"]')))

            size_element.click()
            print(f"Size '{size}' selected successfully!")
            return size
        except Exception as e:
            print("Error:", e)

    def add_to_basket(self):
        """Sepete ekler"""
        try:
            wait = WebDriverWait(self.driver, 10)
            add_to_basket = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'add-to-basket')))
            add_to_basket.click()
        except Exception as e:
            print(f"Ürünü sepete eklerken hata oluştu: {e}")
            raise e