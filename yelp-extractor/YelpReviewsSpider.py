import scrapy
import urllib.parse


class ReviewItem(scrapy.Item):
    restaurant_id = scrapy.Field()
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
        for b_id in ids:
            self.start_urls.append(self.base_url + b_id)

    def parse(self, response):
        yield from self.parse_reviews(response)

        next_link = response.css('a.next::attr("href")').extract_first()
        if next_link is not None:
            yield scrapy.Request(next_link, callback=self.parse)

    def parse_reviews(self, response):
        restaurant_id = response.url.split("/")[-1].split("?")[0]
        restaurant_id = urllib.parse.unquote(restaurant_id)
        for review_obj in response.css('div.review-list ul.reviews li div.review:not(.js-war-widget)'):
            review = ReviewItem()

            review['restaurant_id'] = restaurant_id
            review['review_id'] = review_obj.css('div.review::attr("data-review-id")').extract_first()
            raw_text = review_obj.css('div.review-content p::text').extract()
            review['review_text'] = "".join(raw_text)
            review['review_date'] = review_obj.css('span.rating-qualifier::text').extract_first().strip()
            raw_rating = review_obj.css('div.biz-rating i::attr("title")').extract_first().split(" ")
            review['review_rating'] = float(raw_rating[0])

            raw_user = review_obj.css('div.review-sidebar li.user-name a')
            raw_user_id = raw_user.css('::attr("href")').extract_first().split("=")
            review['user_id'] = raw_user_id[1]
            review['user_name'] = raw_user.css('::text').extract_first()

            review['review_votes'] = self.parse_votes(review_obj.css('ul.voting-buttons li'))
            yield review

    @staticmethod
    def parse_votes(response):
        votes = ReviewVotes()

        for button in response:
            vote_type = button.css('span.vote-type::text').extract_first().lower()
            vote_count = button.css('span.count::text').extract_first()
            votes[vote_type] = int(vote_count) if vote_count is not None else 0

        return votes
