import requests
from lxml import html
from pprint import pprint
from pymongo import MongoClient
from datetime import date, timedelta
import re

client = MongoClient('127.0.0.1', 27017)
db = client['yandex_news']
news = db.news

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}

response = requests.get('https://yandex.ru/news', headers=header)

dom = html.fromstring(response.text)

items = dom.xpath("//div[contains(@class,'mg-card_flexible')]")

for item in items:
    item_info = {}

    source = item.xpath(".//span[@class='mg-card-source__source']/a//text()")[0]
    name = item.xpath(".//h2[@class='mg-card__title']/a//text()")[0].replace('\xa0', ' ')
    link = item.xpath(".//h2[@class='mg-card__title']/a/@href")[0]
    publication_date = item.xpath(".//span[@class='mg-card-source__time']/text()")[0]

    if re.match('^\d{2}:\d{2}$', publication_date) is not None:
        publication_date = date.today().strftime("%d.%m.%Y")
    else:
        publication_date = (date.today() - timedelta(1)).strftime("%d.%m.%Y")

    item_info['source'] = source
    item_info['name'] = name
    item_info['link'] = link
    item_info['publication_date'] = publication_date

    if not news.find_one({'link': item_info['link']}):
        news.insert_one(item_info)

for doc in news.find({}):
    pprint(doc)
