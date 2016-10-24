from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

from Jsonify import jsonify


def businesses_with_menus(creds, params, limit=20):
    auth = Oauth1Authenticator(**creds)
    client = Client(auth)

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

    return [jsonify(x) for x in businesses]
