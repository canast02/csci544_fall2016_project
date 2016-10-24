import scrapy


class YelpMenuSpider(scrapy.Spider):
    name = "menus"
    base_url = 'https://www.yelp.com/menu/'
    start_urls = []

    def __init__(self, ids):
        super().__init__()

        self.ids = ids
        for b_id in ids:
            self.start_urls.append(self.base_url + b_id)

    def parse(self, response):
        # TODO parse web response
        pass

    def parse_menu(self, response):
        # TODO parse menu
        # see example at https://www.yelp.com/menu/tbla-catering-and-cafe-los-angeles/
        pass
