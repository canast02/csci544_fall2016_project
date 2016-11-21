import time
from nltk import tokenize
from nltk.sentiment.vader import SentiText, SentimentIntensityAnalyzer

import json


def main():
    reviews_file = "../yelp-dataset/reviews.json"

    with open(reviews_file, 'r') as f:
        reviews = json.load(f)

    num_reviews = len(reviews)

    analyzer = SentimentIntensityAnalyzer()

    start = time.time()
    sentiment = dict()
    i = 0
    for review in reviews:
        i += 1
        if i % 30 == 0:
            print("\r{:3f}%".format(i/num_reviews * 100), end='')

        review_id = review['review_id']
        review_text = review['review_text']

        s = analyzer.polarity_scores(review_text)
        if review_id in sentiment:
            sentiment[review_id].append(s)
        else:
            l = list()
            l.append(s)
            sentiment[review_id] = l

    print("\r{:.4f}%".format(i / num_reviews * 100), end='')
    print("Done")

    end = time.time()
    print("Sentiment analysis took {} sec".format(end - start))

if __name__ == '__main__':
    main()
