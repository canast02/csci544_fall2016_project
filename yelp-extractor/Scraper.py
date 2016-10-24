import scrapy
from scrapy.crawler import CrawlerProcess


class ReviewsSpider(scrapy.Spider):
    name = "ReviewsSpider"
    start_urls = []

    def __init__(self, ids):
        super().__init__()

        self.ids = ids
        # TODO create urls

    def parse(self, response):
        pass

    def parse_review(self, response):
        pass


class MenuSpider(scrapy.Spider):
    name = "MenuSpider"
    start_urls = []

    def __init__(self, ids):
        super().__init__()

        self.ids = ids
        # TODO create urls

    def parse(self, response):
        pass

    def parse_menu(self, response):
        pass


def scrape_ids(ids):
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    })

    process.crawl(ReviewsSpider, ids)
    process.crawl(MenuSpider, ids)
    process.start()
