# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyprojectItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    link = scrapy.Field()
    authors = scrapy.Field()
    base_price = scrapy.Field()
    discount_price = scrapy.Field()
    rate = scrapy.Field()
    _id = scrapy.Field()

