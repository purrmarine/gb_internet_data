# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class ScrapyprojectPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.book

    def process_item(self, item, spider):
        item['title'] = item['title'][item['title'].find(':') + 2:] if item['authors'] else item['title']
        item['base_price'] = int(item['base_price'])
        item['discount_price'] = int(item['discount_price']) if item['discount_price'] else item['discount_price']
        collection = self.mongo_base[spider.name]

        if not collection.find_one({'link': item['link']}):
            collection.insert_one(item)

        return item
