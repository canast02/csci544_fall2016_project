import scrapy


class YelpReviewsSpider(scrapy.Spider):
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
