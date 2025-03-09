import unittest
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from generic import initialize
from pages.product_page import ProductPage


class TestProductSelection(unittest.TestCase):

    def setUp(self):
        """Tarayıcı başlatılır ve test için hazırlanır."""
        print("\n🔄 Tarayıcı başlatılıyor...")
        self.driver = initialize.run()
        self.driver.get(
            "https://www.trendyol.com/yma-triko/a-t-y-xx-007-v-yaka-sac-orgu-p-863363874?merchantId=923563&boutiqueId=61")

    def test_select_product_options(self):
        """Ürün sayfasında renk ve beden seçimi yapılabiliyor mu?"""
        print("✅ Ürün sayfasına gidiliyor...")

        try:
            WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.CLASS_NAME, 'overlay'))).click()
        except:
            print("ℹ️ Herhangi bir overlay bulunamadı, devam ediliyor.")

        product_page = ProductPage(self.driver)


        print("🎨 Renk seçimi yapılıyor...")
        color = product_page.select_color()
        self.assertIsNotNone(color, "❌ Renk seçimi başarısız!")


        print("📏 Beden seçimi yapılıyor...")
        size = product_page.select_size()
        self.assertIsNotNone(size, "❌ Beden seçimi başarısız!")

        print("✅ Ürün seçenekleri başarıyla seçildi.")

    def tearDown(self):
        """Tarayıcı kapatılır."""
        print("🛑 Tarayıcı kapatılıyor...")
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
