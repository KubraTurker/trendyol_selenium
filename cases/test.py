from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By

from datas.cart_item import CartItem
from generic import initialize, auth


def main():
    driver = initialize.run()
    auth.run(driver)
    sleep(1)
    driver.get("https://www.trendyol.com/sepet")
    # sleep(20)

    cartitems = []
    product_elements = driver.find_elements(By.CLASS_NAME, 'pb-basket-item-wrapper-v2')

    for product in product_elements:
        name = product.find_element(By.CLASS_NAME, 'pb-item').get_attribute('title')
        count = product.find_element(By.CLASS_NAME, 'counter-content').get_attribute('value')
        price = product.find_element(By.CLASS_NAME, 'pb-basket-item-price').text
        price = price.replace("₺", "").replace("TL", "").replace(" ", "").replace(".", "").replace(",", ".")

        cartitems.append(CartItem(name, float(price), int(count)))


    print (cartitems)



if __name__ == "__main__":
    main()


