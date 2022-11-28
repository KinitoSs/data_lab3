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

# sys.path.insert(0, os.path.dirname(__file__) + "/chromedriver.exe")
sys.path.insert(0, "chromedriver.exe")

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

    print("Парсим...")
    for block in location_blocks:
        title = []
        link = []
        publdate = []
        viewCount = []
        data = []

        block_title_div = block.find("div", {"class": "title"}).find("a")

        block_title = block_title_div.find(text=True).strip()
        title.append(block_title)  # заголовок

        block_link = "https://www.news29.ru" + block_title_div.get("href")
        link.append(block_link)  # ссылка

        block_publdate = block.find("div", {"class": "date"}).find(text=True).strip()
        publdate.append(block_publdate)  # дата публикации

        block_viewCount = block.find("div", {"class": "viewscount"}).text.strip()
        if len(block_viewCount.split("\n ")) > 1:
            block_viewCount = block_viewCount.split("\n ")[1]
        elif len(block_viewCount.split("  ")) > 1:
            block_viewCount = block_viewCount.split("  ")[1]
        else:
            block_viewCount = None
        viewCount.append(block_viewCount)  # количество просмотров

        data.append(title[0])
        data.append(link[0])
        data.append(publdate[0])
        data.append(viewCount[0])
        with open("harvest_data.csv", mode="a", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(data)


def click_more_news_button(left=0, right=1000, step=10):
    wait = WebDriverWait(wd, 30)
    print("Ждём, пока кнопка 'Показать еще' будет готова...")
    wait.until(
        EC.element_to_be_clickable((By.ID, "moreNews"))
    )  # Ждем пока кнопка "Показать больше" будет готова
    x = left
    print("Тыкаем на кнопку 'Показать ещё'...")
    while (
        x < right
    ):  # создаем длинный цикл, чтобы проявить статьи вызывающиеся по кнопке "Показать больше"
        time.sleep(0.5)
        wd.execute_script(
            "var moreNewsButton = document.getElementById('moreNews'); "
            "if (moreNewsButton != null) moreNewsButton.click()"
        )
        x = x + step
    time.sleep(2)  # немного ждем, чтобы не потерять последние статьи


click_more_news_button(0, 2000, 10)
parse()

wd.quit()
