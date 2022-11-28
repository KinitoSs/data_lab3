import requests
from lxml import html
from bs4 import BeautifulSoup

url = "https://www.kinopoisk.ru/lists/movies/popular-films/"
header = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
    "application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en,en-US;q=0.9",
    "cache-control": "max-age=0",
    "referer": "https://www.imdb.com/search/title/",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/94.0.4606.71 Safari/537.36 ",
}
r = requests.get(url, headers=header, timeout=(3.05, 27))
# print(r.content)


s = str(r.text.encode("utf-8"))
with open("test.html", "w") as output_file:
    output_file.write(s)

soup = BeautifulSoup(r.text, "html.parser")
film_list = soup.find("div", {"class": "styles_root__ti07r"})

tree = html.fromstring(s)
film_list_lxml = tree.xpath('//*[@id="__next"]/div[2]/div[2]/div[2]/div[3]/main/div')

print(film_list)
print()
print(film_list_lxml)
