import unittest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from generic import initialize, auth
from pages.cart_page import CartPage
from pages.product_page import ProductPage
from time import sleep

class TestAddToCart(unittest.TestCase):

    def setUp(self):
        """Tarayıcı başlatılır ve test için hazırlanır."""
        print("\n🔄 Tarayıcı başlatılıyor...")
        self.driver = initialize.run()

        print("🔑 Kullanıcı giriş yapıyor...")
        auth.run(self.driver)

    def search_product(self, searchkey):
        """Ürün arama işlemi"""
        print(f"🔍 '{searchkey}' kelimesi ile arama yapılıyor...")
        wait = WebDriverWait(self.driver, 10)
        search = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@data-testid = "suggestion"]')))
        search.send_keys(searchkey)
        search.send_keys(Keys.ENTER)
        sleep(2)

    def clicks_first_product(self):
        """Arama sonucundaki ilk ürüne tıklar"""
        wait = WebDriverWait(self.driver, 10)
        try:
            wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'overlay'))).click()
        except:
            print("ℹ️ Pop-up bulunamadı, devam ediliyor.")

        self.driver.execute_script("window.scrollBy(0, 400);")
        first_product = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.p-card-wrppr.with-campaign-view a')))
        first_product.click()
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def go_to_cart(self):
        """Sepete gitme işlemi"""
        wait = WebDriverWait(self.driver, 10)
        go_to_basket = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.account-nav-item.basket-preview')))
        go_to_basket.click()

    def test_add_to_cart(self):
        sleep(3)
        """Ürün sepete eklenebilir mi?"""
        print("✅ Ürün arama testi başlatılıyor...")
        self.search_product(searchkey="kazak")

        print("📌 İlk ürüne tıklanıyor...")
        self.clicks_first_product()
        product_page = ProductPage(self.driver)

        # Pop-up kapatma
        try:
            wait = WebDriverWait(self.driver, 10)
            element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'overlay')))
            element.click()
        except:
            print("ℹ️ Pop-up kapatma gerekmedi.")

        print("📌 Ürün bilgileri alınıyor...")
        price = product_page.get_price()

        print("🎨 Renk seçimi yapılıyor...")
        color = product_page.select_color()
        self.assertIsNotNone(color, "❌ Renk seçimi başarısız!")

        print("📏 Beden seçimi yapılıyor...")
        size = product_page.select_size()
        self.assertIsNotNone(size, "❌ Beden seçimi başarısız!")

        name = product_page.get_name()

        sleep(3)
        print("🛒 Ürün sepete ekleniyor...")
        product_page.add_to_basket()
        self.driver.implicitly_wait(5)

        print("📦 Sepete gidiliyor...")
        self.go_to_cart()

        self.driver.implicitly_wait(4)
        cart_page = CartPage(self.driver)

        try:
            wait = WebDriverWait(self.driver, 10)
            element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'overlay')))
            element.click()
        except:
            print("ℹ️ Pop-up kapatma gerekmedi.")

        sleep(1)
        print("🛍️ Sepetteki ürün bilgileri alınıyor...")
        cart_items = cart_page.cart_items()
        self.assertGreater(len(cart_items), 0, "❌ Sepette ürün bulunamadı!")

        cart_names= " ".join(item.name for item in cart_items)
        cart_prices = [item.price for item in cart_items]

        self.assertIn(name, cart_names, f"❌ {name} sepette bulunamadı!")
        self.assertIn(price, cart_prices, f"❌ Fiyat eşleşmesi başarısız! Ürün fiyatı: {price}, Sepetteki fiyatlar: {cart_prices}")

        print("🗑️ Sepet temizleniyor...")
        cart_page.cart_clear()
        sleep(2)

        print("✅ Test başarılı: Ürün sepete eklendi, doğrulandı ve kaldırıldı!")

    def tearDown(self):
        """Tarayıcı kapatılır."""
        print("🛑 Tarayıcı kapatılıyor...")
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
