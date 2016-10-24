import scrapy


class YelpMenuSpider(scrapy.Spider):
    name = "menus"
    start_urls = []

    def __init__(self, ids):
        super().__init__()

        self.ids = ids
        # TODO create urls

    def parse(self, response):
        pass

    def parse_menu(self, response):
        pass
