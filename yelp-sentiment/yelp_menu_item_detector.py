import json

import nltk
import time

from fuzzywuzzy import fuzz
from fuzzywuzzy import process


def look_for_menu_item(menu, text):
    if len(text) <= 5:
        return

    ltext = text.lower()
    for menu_item in menu:
        lmenu_item = menu_item.lower()
        # exact matching
        if lmenu_item in ltext:
            yield menu_item, text
        # partial matching
        else:
            ext = process.extract(ltext, menu, scorer=fuzz.partial_ratio, limit=5)
            dist1 = fuzz.ratio(lmenu_item, ltext)
            dist2 = fuzz.partial_ratio(lmenu_item, ltext)
            # dist3 = fuzz.partial_token_sort_ratio(lmenu_item, ltext)
            ext = list(filter(lambda x: x[1] > dist2, ext))
            if dist1 > 40 and dist2 > 80 and len(ext) < 2:
                yield menu_item, text


def produce_triples(reviews_file, menus_file, verbose=False):
    if verbose:
        print("Loading datasets...", end="")
    with open(reviews_file, 'r') as f:
        reviews = json.load(f)

    with open(menus_file, 'r') as f:
        menus = json.load(f)

    menus_by_restaurant = dict()
    restaurants = set()
    for m in menus:
        rid = m['restaurant_id']
        restaurants.add(rid)
        menus_by_restaurant.setdefault(rid, set())
        menus_by_restaurant[rid].add(m['name'])

    if verbose:
        print("Done")
        print("Will begin analyzing reviews...")

    sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    for review in filter(lambda r: r['restaurant_id'] in restaurants, reviews):
        rtext = review['review_text']
        rid = review['restaurant_id']
        menu = menus_by_restaurant[rid]
        for sent in sent_tokenizer.tokenize(rtext):
            for menu_item, text in look_for_menu_item(menu, sent):
                yield rid, menu_item, text


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
