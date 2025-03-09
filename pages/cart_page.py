from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datas.cart_item import CartItem


class CartPage:
    def __init__(self, driver):
        self.driver = driver

    def get(self):
        """Sepet sayfasına gitme"""
        self.driver.get("https://www.trendyol.com/sepet")

    def cart_items(self):
        """Sepetteki ürünleri alma"""
        cartitems = []
        product_elements = self.driver.find_elements(By.CLASS_NAME, 'pb-basket-item-wrapper-v2')

        for product in product_elements:
            name = product.find_element(By.CLASS_NAME, 'pb-item').get_attribute('title')
            count = product.find_element(By.CLASS_NAME, 'counter-content').get_attribute('value')
            price = product.find_element(By.CLASS_NAME, 'pb-basket-item-price').text
            price = price.replace( "TL", "").replace(" ", "").replace(".", "").replace(",", ".")

            cartitems.append(CartItem(str(name), float(price), int(count)))

        return cartitems

    def total(self):
        """Sepetteki toplam tutarı alır"""
        total = self.driver.find_element(By.XPATH, '//*[@id="pb-container"]/aside/div/div[2]/ul/li[1]/strong').text
        total = total.replace("TL", "").replace(" ", "").replace(".", "").replace(",", ".")
        return float(total)

    def shipping(self):
        """Kargo ücretini alır"""
        shipping = self.driver.find_element(By.XPATH, '//*[@id="pb-container"]/aside/div/div[2]/ul/li[2]/strong')
        shipping = shipping.text.replace("TL", "").replace(" ", "").replace(".", "").replace(",", ".")
        return float(shipping)

    def discount(self):
        """İndirim tutarını alır"""
        discount = self.driver.find_element(By.CLASS_NAME, 'checkout-saving-wrapper').get_attribute('data-saving-price')
        discount = discount.replace("TL", "").replace(" ", "").replace(".", "").replace(",", ".")
        return float(discount)

    def grand_total(self):
        """Genel toplamı hesaplar (Toplam + Kargo - İndirim)"""
        total_price = self.total()
        shipping_price = self.shipping()
        discount_price = self.discount()
        grand_total = total_price + shipping_price - discount_price
        return grand_total

    def cart_clear(self):
        """Sepeti temizler"""
        wait = WebDriverWait(self.driver, 1)
        clear = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'i-trash')))
        clear.click()