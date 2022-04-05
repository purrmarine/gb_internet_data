import scrapy
from scrapy.http import HtmlResponse
from castoramaparser.items import CastoramaparserItem
from scrapy.loader import ItemLoader


class CastoramaSpider(scrapy.Spider):
    name = 'castorama'
    allowed_domains = ['castorama.ru']
    # start_urls = ['https://www.castorama.ru/catalogsearch/result/?q=зеркало']

    def __init__(self, **kwards):
        super().__init__(**kwards)

        self.start_urls = [f"https://www.castorama.ru/catalogsearch/result/?q={kwards.get('search')}"]

    def parse(self, response: HtmlResponse):

        next_page = response.xpath("//a[@class='next i-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//a[@class='product-card__name ga-product-card-name']")
        for link in links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=CastoramaparserItem(), response=response)
        loader.add_value("link", response.url)
        loader.add_xpath("name", "//h1[@itemprop='name']/text()")
        loader.add_xpath("price", "//span[@class='price']/span/span/text()")
        loader.add_xpath("photos", "//img[@class='top-slide__img swiper-lazy']/@data-src")
        yield loader.load_item()

