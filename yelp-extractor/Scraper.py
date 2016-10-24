from scrapy import signals
from scrapy.exporters import JsonItemExporter
from scrapy.crawler import CrawlerProcess

from YelpMenuSpider import YelpMenuSpider
from YelpReviewsSpider import YelpReviewsSpider


class YelpPipeline(object):
    def __init__(self):
        self.files = {}
        self.exporters = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file = open('{}.json'.format(spider.name), 'wb')
        self.files[spider.name] = file
        self.exporters[spider.name] = JsonItemExporter(file)
        self.exporters[spider.name].start_exporting()

    def spider_closed(self, spider):
        exporter = self.exporters.pop(spider.name)
        exporter.finish_exporting()
        file = self.files.pop(spider.name)
        file.close()

    def process_item(self, item, spider):
        self.exporters[spider.name].export_item(item)
        return item


def scrape_ids(ids):
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
        'ITEM_PIPELINES': {
            'Scraper.YelpPipeline': 0
        }
    })

    process.crawl(YelpReviewsSpider, ids)
    process.crawl(YelpMenuSpider, ids)
    process.start()
