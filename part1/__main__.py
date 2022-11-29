import csv
import bs4
import lxml
import requests
from bs4 import BeautifulSoup
from lxml import html


class SoupParser:
    book_list: list
    __current_book: bs4.element.Tag

    def __init__(self, soup):
        self.book_list = soup.findAll("div", {"class": "genres-carousel__item"})

    def parse_book_list(self, output_file: str):
        for book in self.book_list:
            self.__current_book = book
            data = self.__get_book_data()

            with open(output_file, mode="a", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                writer.writerow(data)

    def __get_book_data(self) -> list:
        data = [self.__get_book_title(), self.__get_book_price(), self.__get_book_author(), self.__get_book_pubhouse()]
        return data

    def __get_book_title(self) -> str:
        try:
            return self.__current_book \
                .find("span", {"class": "product-title"}) \
                .find(text=True) \
                .strip()
        except AttributeError:
            return ""

    def __get_book_price(self) -> int:
        try:
            return int(self.__current_book
                       .find("span", {"class": "price-val"})
                       .find("span").find(text=True)
                       .strip()
                       .replace(" ", ""))
        except AttributeError:
            return 0
        except ValueError:
            return 0

    def __get_book_author(self) -> str:
        try:
            return self.__current_book \
                .find("div", {"class": "product-author"}) \
                .find("a") \
                .find("span") \
                .find(text=True) \
                .strip()
        except AttributeError:
            return ""

    def __get_book_pubhouse(self) -> str:
        try:
            return self.__current_book \
                .find("a", {"class": "product-pubhouse__pubhouse"}) \
                .find("span") \
                .find(text=True) \
                .strip()
        except AttributeError:
            return ""

    def __get_book_series(self):
        try:
            return self.__current_book \
                .find("a", {"class": "product-pubhouse__series"}) \
                .find("span") \
                .find(text=True) \
                .strip()
        except AttributeError:
            return ""


class LxmlParser:
    book_list: list
    __current_book: lxml.html.HtmlElement

    def __init__(self, tree):
        self.book_list = tree.xpath('//*[@id="catalog"]/div/div[3]/div/div[4]/div/div')

    def parse_book_list(self, output_file: str):
        for book in self.book_list:
            self.__current_book = book

            data = self.__get_book_data()

            with open(output_file, mode="a", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                writer.writerow(data)

    def __get_book_data(self) -> list:
        data = [self.__get_book_title(), self.__get_book_price(), self.__get_book_author(), self.__get_book_pubhouse()]
        return data

    def __get_book_title(self) -> str:
        try:
            return self.__current_book.xpath("./div/div[1]/a/span/text()")[0].strip()
        except AttributeError:
            return ""
        except IndexError:
            return ""

    def __get_book_price(self) -> int:
        try:
            return int(self.__current_book.xpath('./div/div[1]/div/div[2]/div/div/span[1]/span/text()')[0]
                       .strip().replace(' ', ''))
        except AttributeError:
            return 0
        except ValueError:
            return 0
        except IndexError:
            return 0

    def __get_book_author(self) -> str:
        try:
            return self.__current_book.xpath('./div/div[2]/a/span/text()')[0].strip()
        except AttributeError:
            return ""
        except IndexError:
            return ""

    def __get_book_pubhouse(self) -> str:
        try:
            return self.__current_book.xpath('./div/div[3]/a[1]/span/text()')[0].strip()
        except AttributeError:
            return ""
        except IndexError:
            return ""

    def __get_book_series(self):
        try:
            return self.__current_book.xpath("./div/div[3]/a[2]/span/text()")[0].strip()
        except AttributeError:
            return ""
        except IndexError:
            return ""


for page in range(1, 18):
    print("Парсинг страницы ", page)
    url = "https://www.labirint.ru/books/?page=" + str(page)
    header = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
                  "application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "ru,en;q=0.9",
        "cache-control": "max-age=0",
        "cookie": "id_post=1964; UserSes=lab4e64cs6t7uhq34p; br_webp=8; PHPSESSID=vlsb1aet59uu2l1sd3dbdohjqs; "
                  "referrer=https%3A%2F%2Fyandex.ru%2F; begintimed=MTY2OTcxNjc1MQ%3D%3D; banner-catalog-cashback-11671=1; "
                  "cookie_policy=1",
        "sec-ch-ua": '"Chromium";v="106", "Yandex";v="22", "Not;A=Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 "
                      "YaBrowser/22.11.0.2500 Yowser/2.5 Safari/537.36",
    }

    r = requests.get(url, headers=header, timeout=(3.05, 27))
    r.encoding = 'utf-8'

    soup = BeautifulSoup(r.text, "html.parser")
    book_list = soup.findAll("div", {"class": "genres-carousel__item"})

    tree = html.fromstring(r.text)
    book_list_lxml = tree.xpath('//*[@id="catalog"]/div/div[3]/div/div[4]/div/div')

    SoupParser(soup).parse_book_list("soup_parse_result.csv")
    LxmlParser(tree).parse_book_list("lxml_parse_result.csv")
