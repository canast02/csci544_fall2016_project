import json
import urllib.parse
from unidecode import unidecode


def main():
    with open('businesses.json') as f:
        jb = json.load(f)
    with open('menus.json') as f:
        jm = json.load(f)
    with open('reviews.json') as f:
        jr = json.load(f)

    ub = set()
    for i in jb:
        ub.add(i['id'])
    ur = set()
    for i in jm:
        ur.add(urllib.parse.unquote(i['restaurant_id']))

    print('{} businesses'.format(len(ub)))
    print('{} restaurants'.format(len(ur)))

    diff = ub - ur
    print(diff)

    b = list(filter(lambda x: x['id'] not in diff, jb))
    r = list(filter(lambda x: x['restaurant_id'] not in diff, jr))

    for x in r:
        x['review_text'] = unidecode(x['review_text'])
    for x in jm:
        x['name'] = unidecode(x['name'])
        x['description'] = unidecode(x['description'])

    with open('businesses.json', 'w') as f:
        json.dump(b, f, indent=2)
    with open('reviews.json', 'w') as f:
        json.dump(r, f, indent=2)
    with open('menus.json', 'w') as f:
        json.dump(jm, f, indent=2)

if __name__ == '__main__':
    main()
