import scrapy
import urllib.parse


class MenuItem(scrapy.Item):
    name = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
    restaurant_id = scrapy.Field()


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
        yield from self.parse_menu(response)

        for submenu in response.css('ul.sub-menus li a'):
            page = submenu.css('::attr("href")').extract_first()
            yield scrapy.Request("https://www.yelp.com"+page, callback=self.parse_menu)

    def parse_menu(self, response):
        restaurant_id = response.url.split("/")[4]
        restaurant_id = urllib.parse.unquote(restaurant_id)
        for item in response.css('div.menu-section div.menu-item'):
            menu_item = self.parse_menu_item(item)
            menu_item['restaurant_id'] = restaurant_id
            yield menu_item

    @staticmethod
    def parse_menu_item(item):
        menu_item = MenuItem()

        menu_item['name'] = "".join(item.css('h4 ::text').extract()).strip()
        desc = item.css('p.menu-item-details-description::text').extract_first()
        if desc is not None:
            menu_item['description'] = desc.strip()
        else:
            menu_item['description'] = ''
        price = item.css('div.menu-item-prices .menu-item-price-amount::text').extract_first()
        if price is not None:
            menu_item['price'] = price.strip()
        else:
            menu_item['price'] = ''

        return menu_item
