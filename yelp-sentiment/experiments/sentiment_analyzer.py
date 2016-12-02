import json
import time

import nltk
import sys
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def main():
    reviews_file = sys.argv[1]
    output_file = sys.argv[2]

    print('Loading reviews from file "{}"'.format(reviews_file), end='')
    with open(reviews_file, 'r') as f:
        reviews = json.load(f)
    print('Done')

    num_reviews = len(reviews)

    analyzer = SentimentIntensityAnalyzer()
    sent_tok = nltk.data.load('tokenizers/punkt/english.pickle')

    start = time.time()
    sentiment = dict()
    i = 0
    for review in reviews:
        i += 1
        if i % 30 == 0:
            print("\r{:3f}%".format(i/num_reviews * 100), end='')

        review_id = review['review_id']
        review_text = review['review_text']

        l = []
        for sentence in sent_tok.tokenize(review_text):
            s = analyzer.polarity_scores(sentence)
            s['text'] = sentence
            l.append(s)
        sentiment[review_id] = l

    print("\r{:.4f}%".format(i / num_reviews * 100), end='')
    print("Done")

    end = time.time()
    print("Sentiment analysis took {} sec".format(end - start))

    with open(output_file, 'w') as f:
        json.dump(sentiment, f, indent=2)

if __name__ == '__main__':
    main() 
