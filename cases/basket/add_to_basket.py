from selenium.webdriver.support.wait import WebDriverWait
from generic import initialize, auth
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


def search_product(driver, searchkey):

    search = driver.find_element(By.XPATH, '//*[@data-testid = "suggestion"]')
    search.send_keys(searchkey)
    search.send_keys(Keys.ENTER)

def product_order(driver, sort):

    order = driver.find_element(By.CLASS_NAME, 'search-sort-container')
    order.click()
    sortproduct = order.find_element(By.XPATH, "//span[contains(text(), '{}')]".format(sort))
    sortproduct.click()


def clicks_first_product(driver):
    wait = WebDriverWait(driver, 1000)
    first_product = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,  '.p-card-wrppr.with-campaign-view')))
    first_product.click()

def campaign_product_check(driver):
    print('campaign_product_check')
    print(driver.current_window_handle)
    print(driver.window_handles)
    driver.switch_to.window(driver.window_handles[-1])
    element = WebDriverWait(driver, 3000).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.overlay'))
    )

    element.click()

    wait = WebDriverWait(driver, 1000)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.product-price-container .prc-dsc'))).text

def add_to_basket(driver):
    wait = WebDriverWait(driver, 1000)
    add_basket = wait.until(EC.visibility_of_element_located((By.CLASS_NAME,'add-to-basket-button-text')))
    add_basket.click()

def basket_check(driver):
    wait = WebDriverWait(driver, 1000)
    go_to_basket = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.account-nav-item.basket-preview')))
    go_to_basket.click()

def check_cart_items(driver):
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "pb-basket-item-wrapper-v2")))

    # "pb-basket-item checkout-saving-enabled" sınıfındaki tüm öğeleri al
    product_elements = driver.find_elements(By.CLASS_NAME, "pb-basket-item-wrapper-v2")

    # Ürün başlıklarını ve fiyatlarını saklayacağımız bir set (benzersiz başlıkları tutar)
    product_info = set()
    total_price = 0.0

    # Ürün başlıkları ve fiyatları yazdır
    for product in product_elements:
        try:
            # Başlıkları <span> etiketi içinde alıyoruz
            title_element = product.find_element(By.CLASS_NAME, "pb-item")
            title = title_element.get_attribute('title').strip()  # Başlık metnini al

            # Fiyatı almak için "pb-basket-item-price" class'ını kullanıyoruz
            price_element = product.find_element(By.CLASS_NAME, "pb-basket-item-price")
            price_text = price_element.text.strip()  # Fiyat metnini al

            # Fiyatı sayıya dönüştürmek için para birimi simgesini kaldırıyoruz
            price_text_clean = price_text.replace("₺", "").replace("TL", "").replace(" ", "").replace(",", ".")

            # Sayıya dönüştürmeye çalışıyoruz
            try:
                price_number = float(price_text_clean)
            except ValueError:
                print(f"Fiyat dönüştürülemedi: {price_text_clean}")
                continue  # Eğer dönüştürme hatası olursa, bu ürünü atla

            # Toplam fiyatı ekliyoruz
            total_price += price_number

            # Eğer başlık daha önce eklenmemişse, başlık ve fiyatı ekle
            if (title, price_text) not in product_info:
                product_info.add((title, price_text))  # Başlık ve fiyat çiftini set'e ekle
                print(f"Ürün Başlığı: {title} - Fiyat: {price_text}")  # Benzersiz başlık ve fiyatı yazdır


        except Exception as e:
            print("Başlık veya fiyat bulunamadı:", e)

    print(f"Toplam Fiyat: ₺{total_price:.2f}")

def check_cart_total(driver):
    wait = WebDriverWait(driver, 1000)
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'pb-summary-box')))

    sub_total = driver.find_element(By.XPATH, '//*[@id="pb-container"]/aside/div/div[2]/ul/li[1]/strong').text
    print(sub_total)

    total_shipping = driver.find_element(By.XPATH, '//*[@id="pb-container"]/aside/div/div[2]/ul/li[2]/strong').text
    print(total_shipping)

    discount_element = driver.find_element(By.CLASS_NAME, 'checkout-saving-wrapper')
    discount = discount_element.get_attribute('data-saving-price')
    print(discount)

    grand_total_element = driver.find_element(By.CLASS_NAME, 'pb-summary-total-price.discount-active')
    grand_total = grand_total_element.get_attribute('title')
    return grand_total, total_shipping


def check_cart(driver):

    total_price = check_cart_items(driver)
    (grand_total, total_shipping) = check_cart_total(driver)

    assert total_price == (grand_total + total_shipping), f"Değerler eşit değil: {total_price} != {grand_total + total_shipping}"



def main():

    driver = initialize.run()
    auth.run(driver)
    sleep(5)
    search_product(driver, searchkey='nemlendirici krem')
    product_order(driver, sort='En çok satan')
    clicks_first_product(driver)
    campaign_product_check(driver)
    add_to_basket(driver)
    sleep(5)
    basket_check(driver)
    sleep(3)
    check_cart_items(driver)
    check_cart_total(driver)
    sleep(10)
    driver.quit()

if __name__ == "__main__":
    main()


