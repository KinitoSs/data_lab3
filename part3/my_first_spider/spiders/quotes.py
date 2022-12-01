import scrapy
import csv

base_url = 'http://quotes.toscrape.com/api/quotes?page={}'


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    start_urls = [base_url.format(1)]

    def parse(self, response, **kwargs):
        data = response.json()

        for quote in data['quotes']:
            with open("harvest_data.csv", mode="a", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                writer.writerow([quote['author']['name'], quote['text']])

            yield {
                'Author': quote['author']['name'],
                'Quote': quote['text']
            }
        current_page = data["page"]
        if data['has_next']:
            next_page_url = base_url.format(current_page + 1)
            yield scrapy.Request(next_page_url)
