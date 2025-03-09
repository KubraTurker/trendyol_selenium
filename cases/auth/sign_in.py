# Kullanici login olabiliyor mu kontrolu yapilir
# 1. Ana sayfaya gidilir
# 2. Login Butonuna tiklanir
# 3. Bilgiler girilir
# 4. Hesabim butonuna tiklanir
# 5. Hesabim sayfasinin acildigi dogrulanir
import unittest
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from generic import initialize, auth


class TestUserLogin(unittest.TestCase):

    def setUp(self):
        """Tarayıcı başlatılır ve test için hazırlanır."""
        print("\n🔄 Tarayıcı başlatılıyor...")
        self.driver = initialize.run()
        auth.run(self.driver)

    def click_stable_element(self, by, value, retries=3):
        """Elemente güvenli bir şekilde tıklar, stale olursa tekrar dener."""
        for attempt in range(retries):
            try:
                element = self.driver.find_element(by, value)
                element.click()
                return
            except (StaleElementReferenceException, NoSuchElementException):
                sleep(1)

        raise Exception(f"Element {retries} denemeye rağmen tıklanamadı!")

    def test_user_can_login(self):
        """Kullanıcı başarılı şekilde login olup 'Hesabım' sayfasını görebiliyor mu?"""
        print("✅ Login işlemi başlatılıyor...")

        self.click_stable_element(By.CSS_SELECTOR, ".account-nav-item.user-login-container")

        wait = WebDriverWait(self.driver, 10)
        try:
            account_page_check = wait.until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'section-user_info'))
            )
            self.assertTrue(account_page_check.is_displayed(), "❌ Hesabım sayfası açılmadı!")
            print("✅ Hesabım sayfası başarıyla açıldı.")
        except TimeoutException:
            self.fail("❌ Hesabım sayfası belirtilen süre içinde açılmadı!")

    def tearDown(self):
        """Tarayıcı kapatılır."""
        print("🛑 Tarayıcı kapatılıyor...")
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
