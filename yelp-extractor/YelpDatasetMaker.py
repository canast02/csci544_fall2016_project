import json

from Extractor import businesses_with_menus


def main():
    # read API keys
    with open('config_secret.json') as cred:
        creds = json.load(cred)

    params = {
        'lang': 'en'
    }

    print('Getting businesses with menus from Yelp API...')
    businesses = businesses_with_menus(creds, params, limit=20)
    print('Loaded {} businesses'.format(len(businesses)))

    with open('businesses.json', 'w') as file:
        json.dump(businesses, file, indent=2)
        print("Stored in JSON format")

    business_ids = [r['id'] for r in businesses]


if __name__ == '__main__':
    main()
