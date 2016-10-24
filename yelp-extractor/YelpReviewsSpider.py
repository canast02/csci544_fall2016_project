import scrapy


class ReviewItem(scrapy.Item):
    review_id = scrapy.Field()
    user_id = scrapy.Field()
    user_name = scrapy.Field()
    review_text = scrapy.Field()
    review_rating = scrapy.Field()
    review_date = scrapy.Field()
    review_votes = scrapy.Field()


class ReviewVotes(scrapy.Item):
    useful = scrapy.Field()
    funny = scrapy.Field()
    cool = scrapy.Field()


class YelpReviewsSpider(scrapy.Spider):
    name = "reviews"
    base_url = 'https://www.yelp.com/biz/'
    start_urls = []

    def __init__(self, ids):
        super().__init__()

        self.ids = ids
        # TODO create urls
        for id in ids:
            self.start_urls.append(self.base_url + id)

    def parse(self, response):
        for review_obj in response.css('div.review-list ul.reviews li div.review:not(.js-war-widget)'):
            yield from self.parse_review(review_obj)

        # next_link = response.css('a.next::attr("href")')
        # if next_link is not None:
        #     yield scrapy.Request(next_link.extract_first(), callback=self.parse)

    def parse_review(self, response):
        review = ReviewItem()

        review['review_id'] = response.css('div.review::attr("data-review-id")').extract_first()
        raw_text = response.css('div.review-content p::text').extract()
        review['review_text'] = "".join(raw_text)
        review['review_date'] = response.css('span.rating-qualifier::text').extract_first().strip()
        raw_rating = response.css('div.biz-rating i::attr("title")').extract_first().split(" ")
        review['review_rating'] = float(raw_rating[0])

        raw_user = response.css('div.review-sidebar li.user-name a')
        raw_user_id = raw_user.css('::attr("href")').extract_first().split("=")
        review['user_id'] = raw_user_id[1]
        review['user_name'] = raw_user.css('::text').extract_first()

        review['review_votes'] = self.parse_votes(response.css('ul.voting-buttons'))
        yield review

    def parse_votes(self, response):
        votes = ReviewVotes()

        return votes
