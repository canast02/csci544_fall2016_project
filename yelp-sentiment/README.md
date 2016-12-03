## Yelp Sentiment

### Required python libraries

In order to run the sentiment analyzer you will need to install NLTK and
some of its packages.

```
$ pip install nltk
$ pip install python-Levenshtein
$ pip install fuzzywuzzy
```
Then on the python console run the following:
```
>>> import nltk
>>> nltk.download()
```
A window will open; navigate to all packages and download ```punkt``` and
```vader_lexicon``` .

### Running the extractor

You need to run the ```yelp_sentiment_analyzer.py``` giving three parameters; the
path to the reviews file, the path to the menus file and the filename for the sentiment output.

### Experiments

We have tried performing sentiment analysis classification with the following algorithms:

- Naive Bayes
- Support Vector Machines (Linear and Nu)
- Decision Tree
- Random Forest
- Stochiastic Gradient Descent
- Positive Naive Bayes
- Logistic Regression


