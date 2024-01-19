from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import time

def parser(search: str):
    driver = webdriver.Firefox()
    driver.get(f'https://www.wildberries.ru/catalog/0/search.aspx?search=к{search}')

    time.sleep(2)
    items = driver.find_elements(By.XPATH, "//div[@class='product-card__wrapper']")
    result = []
    # Пройдемся по найденным элементам и получим информацию о каждом продукте
    count = 0
    for item in items:
        if count == 5:
            break
        # Создадим объект ActionChains для выполнения действий с клавишами
        action_chains = ActionChains(driver)

        # Откроем ссылку в новой вкладке (может потребоваться регулировка)
        action_chains.key_down(Keys.CONTROL).click(item).key_up(Keys.CONTROL).perform()

        # Подождем 2 секунды (добавьте необходимую задержку)
        time.sleep(2)

        # Переключимся на новую вкладку
        driver.switch_to.window(driver.window_handles[1])

        # Теперь ищем элементы внутри текущего элемента (item)
        title = driver.find_element(By.XPATH, ".//h1[@class='product-page__title']").text
        price = driver.find_element(By.XPATH, ".//ins[@class='price-block__final-price']").text
        link = driver.current_url
        link_img = driver.find_element(By.XPATH, "//div[@class='slide__content img-plug']//img").get_attribute('src')

        # Добавим информацию в результат
        listItem = {
            "title": title,
            "price": price,
            "link": link,
            "link_img": link_img
        }
        result.append(listItem)
        count += 1
        # Закроем текущую вкладку
        driver.close()

        # Переключимся обратно на предыдущую вкладку
        driver.switch_to.window(driver.window_handles[0])

    driver.close()
    return result

# parser("кросовки nike")