import scrapy
from scrapy.http import HtmlResponse
from scrapyproject.items import ScrapyprojectItem


class LabirintruSpider(scrapy.Spider):
    name = 'labirintru'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/%D0%BF%D1%83%D1%88%D0%BA%D0%B8%D0%BD/?stype=0&available=1&paperbooks=1']

    def parse(self, response: HtmlResponse):
        base_url = 'https://www.labirint.ru'

        next_page = response.xpath("//a[@class='pagination-next__text']/@href").get()
        if next_page:
            next_page = f'{base_url}/books/{next_page}'
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//a[@class='product-title-link']/@href").getall()

        for link in links:
            link = base_url + link
            yield response.follow(link, callback=self.book_parse)

    def book_parse(self, response: HtmlResponse):
        # * Ссылку на книгу
        link = response.url
        # * Наименование книги
        title = response.xpath("//h1/text()").get()
        # * Автор(ы)
        authors = response.xpath("//a[@data-event-label='author']/text()").getall()
        # * Основную цену
        base_price = response.xpath("//span[@class='buying-priceold-val-number']/text()").get()
        if not base_price:
            base_price = response.xpath("//span[@class='buying-price-val-number']/text()").get()
        # * Цену со скидкой
        discount_price = response.xpath("//span[@class='buying-pricenew-val-number']/text()").get()
        # * Рейтинг книги
        rate = response.xpath("//div[@id='rate']/text()").get()
        yield ScrapyprojectItem(title=title, link=link, authors=authors, base_price=base_price, discount_price=discount_price, rate=rate)
