from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from generic import initialize, auth
from time import sleep

from pages.cart_page import CartPage
from pages.product_page import ProductPage


def search_product(driver, searchkey):
    search = driver.find_element(By.XPATH, '//*[@data-testid = "suggestion"]')
    search.send_keys(searchkey)
    search.send_keys(Keys.ENTER)

def clicks_first_product(driver):
    wait = WebDriverWait(driver, 2)
    try:
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'overlay'))).click()
    except:
        pass
    driver.execute_script("window.scrollBy(0, 400);")  # Burada bir hata olmamalı
    first_product = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,  '.p-card-wrppr.with-campaign-view a')))
    print(first_product)
    first_product.click()

def go_to_cart(driver):
    wait = WebDriverWait(driver, 1)
    go_to_basket = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.account-nav-item.basket-preview')))
    go_to_basket.click()

def main():
    driver = initialize.run()
    auth.run(driver)
    sleep(2)
    search_product(driver, searchkey='kazak')
    sleep(1)
    clicks_first_product(driver)
    driver.switch_to.window(driver.window_handles[-1])
    product_page = ProductPage(driver)

    wait = WebDriverWait(driver, 2)

    element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'overlay')))
    element.click()
    # actions = ActionChains(driver)
    # actions.move_to_element_with_offset(element, 200, 200).click().perform()

    sleep(0.2)
    name = product_page.get_name()
    price = product_page.get_price()

    color = product_page.select_color()
    assert color is not None, "AssertionError: Renk seçimi yapılmadı"

    size = product_page.select_size()
    assert size is not None, "AssertionError: Beden seçimi yapılmadı"


    sleep(3)
    product_page.add_to_basket()
    sleep(5)

    go_to_cart(driver)
    sleep(4)
    cart_page = CartPage(driver)
    cart_items = cart_page.cart_items(driver)

    assert len(cart_items) > 0, "AssertionError: Sepette ürün bulunamadı"

    cart_names = [item.name for item in cart_items]
    cart_prices = [item.price for item in cart_items]

    assert any(price == cart_price for cart_price in cart_prices), \
    f"AssertionError:Fiyat eslesmesi yapilamadi. Urun fiyati {price}, sepetteki fiyatlar{cart_prices}"

    assert name in cart_names, f"AssertionError: {name} sepette bulunamadi"
    sleep(2)

    clear = cart_page.cart_clear()

    print("add_to_cart: Success, Test başarılı: Ürün sepete eklendi, doğrulama yapıldı ve sepetten çıkarıldı.")

    driver.quit()




if __name__ == "__main__":
    main()


