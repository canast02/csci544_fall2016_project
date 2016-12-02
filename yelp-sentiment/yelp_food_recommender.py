import random
from argparse import ArgumentParser

import time

from sentiment_util import load_dataset
from yelp_menu_item_detector import produce_triples
from yelp_sentiment_analyzer import YelpSentimentAnalyzer


def create_and_train_analyzer():
    train_x, train_y = load_dataset('datasets/sentiment_uci/yelp_labelled.txt')
    analyzer = YelpSentimentAnalyzer()
    analyzer.fit(train_x, train_y)

    return analyzer


def main():
    argparser = ArgumentParser(description="Yelp Food Recommender")
    argparser.add_argument("reviews", help="The file containing the reviews")
    argparser.add_argument("menus", help="The file containing menus")
    argparser.add_argument("output", help="The file to store the output")
    argparser.add_argument("--verbose", "-v", action="store_true")

    args = argparser.parse_args()

    yelp_sentiment_analyzer = create_and_train_analyzer()
    scores = dict()

    start = time.time()
    if args.verbose:
        print("Analyzing reviews...", end="", flush=True)
        count = 0

    review_filter = lambda x: x['review_rating'] >= 4
    # random_filter = lambda x: random.random() > 0.6
    # both_filter = lambda x: x['review_rating'] >= 4 and random.random() > 0.6
    restaurant_filter = lambda x: random.random() > 0.85  # selecting a random subset of our dataset
    triples = produce_triples(args.reviews, args.menus, review_filter=review_filter,
                              restaurant_filter=restaurant_filter)
    for restaurant, menu_item, review_text in triples:
        sentiment = yelp_sentiment_analyzer.predict([review_text])[0]
        sentiment = sentiment * 2 - 1
        scores.setdefault(restaurant, dict())
        scores[restaurant].setdefault(menu_item, 0)
        scores[restaurant][menu_item] += sentiment

    end = time.time()

    if args.verbose:
        print("Done in {} sec".format(end - start))

    f = open(args.output, 'w')
    f.write("restaurant,top_choices\n")
    if args.verbose:
        print("Writing out the results...", end="", flush=True)

    for restaurant in scores:
        rscores = [(menu_item, score) for menu_item, score in scores[restaurant].items()]
        rscores.sort(key=lambda tup: tup[1], reverse=True)
        rscores = rscores[:10]
        recommendations = list(map(lambda x: x[0], rscores))
        f.write("{}, [{}]\n".format(restaurant, ", ".join(recommendations)))

    f.close()
    if args.verbose:
        print("Done")


if __name__ == '__main__':
    main()
