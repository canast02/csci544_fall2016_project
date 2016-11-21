## Yelp Sentiment

### Required python libraries

In order to run the sentiment analyzer you will need to install NLTK and
some of its packages.

```
$ pip install nltk
```
Then on the python console run the following:
```
>>> import nltk
>>> nltk.download()
```
A window will open; navigate to all packages and download ```punkt``` and
```vader_lexicon```.

### Running the extractor

You need to run the ```sentiment_analyzer.py``` giving two parameters; the
path to the reviews file and the filename for the sentiment output.
