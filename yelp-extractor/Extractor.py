import json

from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator


def restaurants_with_menus(client, params, limit=20):
    businesses = []
    has_menu = lambda r: r.menu_provider is not None

    iteration = 0
    while len(businesses) < limit:
        params['offset'] = iteration * 20
        response = client.search('Los Angeles', **params)
        if len(response.businesses) <= 0:
            break
        with_menus = list(filter(has_menu, response.businesses))
        businesses += with_menus

    return businesses


def main():
    # read API keys
    with open('config_secret.json') as cred:
        creds = json.load(cred)
        auth = Oauth1Authenticator(**creds)
        client = Client(auth)

    params = {
        'lang': 'en'
    }

    restaurants = restaurants_with_menus(client, params, limit=20)
    print(restaurants)

    print(restaurants[0]._fields)
    attrs = {key: value for key, value in restaurants[0].__dict__.items()}
    print(attrs)

if __name__ == '__main__':
    main()
