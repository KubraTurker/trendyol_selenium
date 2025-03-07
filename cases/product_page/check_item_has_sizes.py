from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from generic import initialize
from pages.product_page import ProductPage


def main():
    driver = initialize.run()
    driver.get("https://www.trendyol.com/yma-triko/a-t-y-xx-007-v-yaka-sac-orgu-p-863363874?merchantId=923563&boutiqueId=61")
    WebDriverWait(driver, 1000).until(EC.presence_of_element_located((By.CLASS_NAME, 'overlay'))).click()

    product_page = ProductPage(driver)

    print(product_page.get_sizes())
    print(product_page.get_colors())
    product_page.select_size('L')

if __name__ == "__main__":
    main()


