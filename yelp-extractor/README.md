## Yelp Data Extractor

### Required python libraries

In order to run the extractor you will need to install yelp-python and scrapy.

```
$ pip install yelp  
$ pip install scrapy
```

### Setup

Create a file named config_secret.json with your Yelp API keys.

```
{
    "consumer_key": "YOUR_CONSUMER_KEY",
    "consumer_secret": "YOUR_CONSUMER_SECRET",
    "token": "YOUR_TOKEN",
    "token_secret": "YOUR_TOKEN_SECRET"
}
```

### Running the extractor

All you have to do is run ```YelpDatasetMaker.py```. You can optionally set the querying params 
and the number of businesses you want to extract. If the execution is successful you should
see three JSON files; ```businesses.json```, ```reviews.json``` and ```menus.json```.
