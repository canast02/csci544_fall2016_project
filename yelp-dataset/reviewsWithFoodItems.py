import json, sets, re

foodwords = set()
rr4to5 = {}

'''Read the menus.json file and for each of the food items names, 
split them and add them as set elements to the set foodwords'''
with open('menus.json') as data_file:    
    menus = json.load(data_file)
    for each in menus:
        dish = each["name"]
        dishgrams = re.compile('\w+').findall(dish)
        foodwords = foodwords.union(set(dishgrams))

'''Read the reviews.json file and check for all reviews that have 4 or 5 star rating'''
with open('reviews.json') as data_file:    
    reviews = json.load(data_file)
    for each in reviews:
        if float(each["review_rating"]) == 4 or float(each["review_rating"]) == 5:
            rr4to5[each["review_id"]] = each["review_text"]

'''Now with the filtered set of reviews, check if there are food items
in the reviews. This is done by checking out if the length of the intersection
of the foodwords and the words in the reviews is greater than 0'''
ks = rr4to5.keys()
for each in ks:
    revgrams = re.compile('\w+').findall(rr4to5[each])
    if len(foodwords.intersection(revgrams)) == 0:
        del rr4to5[each]
