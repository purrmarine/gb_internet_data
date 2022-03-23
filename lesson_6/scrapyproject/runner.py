from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from scrapyproject import settings
from scrapyproject.spiders.labirintru import LabirintruSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    crawler_process = CrawlerProcess(settings=crawler_settings)
    crawler_process.crawl(LabirintruSpider)

    crawler_process.start()