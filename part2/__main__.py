# импортим библиотеки
import os
import requests
import time
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import sys

URL = "https://www.news29.ru/novosti/ekonomika/"

sys.path.insert(0, os.path.dirname(__file__) + "/chromedriver.exe")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

wd = webdriver.Chrome("chromedriver", options=chrome_options)
wd.get(URL)
wd.implicitly_wait(10)
wd.fullscreen_window()
print(wd.title)  # проверяем работу


def write_html_page_to_file(html_page: str, filename: str):
    with open(filename, "w", encoding="cp1251") as f:
        f.write(html_page)


write_html_page_to_file(wd.page_source, "source_page.html")


def parse():
    soup = BeautifulSoup(
        wd.page_source, features="lxml"
    )  # создание объекта BeautifulSoup для работы с DOM моделью. Используем
    # данные с selenium
    location_blocks = soup.findAll(
        "div", {"class": "newItemContainer"}
    )  # получение всех div с классом 'newItemContainer', который содержит всю необходимую информацию

    for block in location_blocks:
        link = []
        title = []
        publdate = []
        viewCount = []
        tags = []
        tagsAll = []
        data = []

        block_title = block.find("div").find(
            "a", {"class": "list-item__title color-font-hover-only"}
        )
        if block_title is not None:
            title.append(block_title) # заголовок

        link.append(
            block.find("a", {"class": "list-item__title color-font-hover-only"}).get(
                "href"
            )
        )  # Ссылка

        block_title = block.find("div", {"class": "list-item__info"}).find(
            "div", {"class": "list-item__date"}
        )
        if block_title is not None:
            publdate.append(block_title)  # дата публикации

        block_viewCount = (
            block.find("div", {"class": "list-item__info"})
            .find("div", {"class": "list-item__views"})
            .find("div", {"class": "list-item__views-text"})
        )
        if block_viewCount is not None:
            block_viewCount.append(block_viewCount)  # количество просмотров

        tagsAll = block.find("ul")  # берем весь список тегов
        for itemLi in tagsAll:
            tags.append(itemLi.find("a").text)  # раскидываем каждый элемент

        data.append(title)
        data.append(link)
        data.append(publdate)
        data.append(viewCount)
        data.append(tags)
        with open("harvest_data.csv", mode="a", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(data)


wait = WebDriverWait(wd, 30)
# wait.until(
#     EC.element_to_be_clickable((By.CLASS_NAME, "list-more"))
# )  # Ждем пока кнопка "Показать больше" будет готова

# x = 0
# while (
#     x < 2000
# ):  # создаем длинный цикл, чтобы проявить статьи вызывающиеся по кнопке "Показать больше"
#     time.sleep(0.5)
#     wd.execute_script(
#         'document.querySelector("#content > div > div.layout-rubric__main > div > div.list-more").click()'
#     )  # Имитируем нажатие на кнопку исполняя скрипт с указанием click()
#     x = x + 10

time.sleep(2)  # немного ждем, чтобы не потерять последние статьи
parse()

wd.quit()
