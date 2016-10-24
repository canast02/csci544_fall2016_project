from scrapy.crawler import CrawlerProcess

from YelpMenuSpider import  YelpMenuSpider
from YelpReviewsSpider import YelpReviewsSpider


def scrape_ids(ids):
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    })

    process.crawl(YelpReviewsSpider, ids)
    process.crawl(YelpMenuSpider, ids)
    process.start()
