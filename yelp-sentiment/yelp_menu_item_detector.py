import json

import nltk
import time

import sys
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


def look_for_menu_item(menu, text):
    if len(text) <= 5:
        return

    found_items = set()
    ltext = text.lower()
    # exact matching
    for menu_item in menu:
        lmenu_item = menu_item.lower()
        if lmenu_item in ltext:
            yield menu_item, text
            found_items.add(menu_item)

    # if we already found more than two items let's stop searching
    if len(found_items) > 2:
        return

    # partial matching
    rest_items = [i for i in menu if i not in found_items]
    ext1 = process.extract(ltext, rest_items, scorer=fuzz.partial_ratio, limit=5)
    ext2 = process.extract(ltext, rest_items, scorer=fuzz.token_set_ratio, limit=5)

    ext1 = set(map(lambda x: x[0], filter(lambda x: x[1] > 80, ext1)))
    ext2 = set(map(lambda x: x[0], filter(lambda x: x[1] > 40, ext2)))

    ext = ext1.intersection(ext2)

    for menu_item in ext:
        yield menu_item, text


def produce_triples(reviews_file, menus_file, review_filter=None, restaurant_filter=None, verbose=False):
    if verbose:
        print("Loading datasets...", end="")
    with open(reviews_file, 'r') as f:
        reviews = json.load(f)
        if review_filter is not None:
            reviews = list(filter(review_filter, reviews))

    with open(menus_file, 'r') as f:
        menus = json.load(f)

    menus_by_restaurant = dict()
    restaurants = set()
    for m in menus:
        rid = m['restaurant_id']
        restaurants.add(rid)
        menus_by_restaurant.setdefault(rid, set())
        menus_by_restaurant[rid].add(m['name'])

    if restaurant_filter is not None:
        restaurants = set(filter(restaurant_filter, restaurants))

    if verbose:
        print("Done")
        print("Will begin analyzing reviews...")

    sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    reviews = list(filter(lambda r: r['restaurant_id'] in restaurants, reviews))
    count = 0.0
    n_reviews = len(reviews)
    sys.stderr.write("0.0")
    for review in reviews:
        count += 1
        sys.stderr.write("\r{}".format(count / n_reviews))
        rtext = review['review_text']
        rid = review['restaurant_id']
        menu = menus_by_restaurant[rid]
        for sent in sent_tokenizer.tokenize(rtext):
            for menu_item, text in look_for_menu_item(menu, sent):
                yield rid, menu_item, text
    sys.stderr.write("\r1.0\n")


def main():
    reviews_file = "../yelp-dataset/reviews.json"
    menus_file = "../yelp-dataset/menus.json"

    produce_triples(reviews_file, menus_file)

    f = open('triples.csv', 'w')
    f.write('restaurant_id,menu_item,text\n')
    count = 0
    print("Working on it...Please wait...")
    start = time.time()
    for restaurant, menu_item, review_text in produce_triples(reviews_file, menus_file):
        f.write('{},{},{}\n'.format(restaurant, menu_item, review_text))
        count += 1
        print([restaurant, menu_item, review_text])
    f.close()

    end = time.time() 
    print("Found {} triples in {} sec".format(count, end - start))

if __name__ == '__main__':
    main()
