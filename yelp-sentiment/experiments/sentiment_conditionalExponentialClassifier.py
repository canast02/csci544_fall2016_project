import numpy as np
from nltk import TweetTokenizer
from nltk.classify import MaxentClassifier
from nltk.classify.maxent import ConditionalExponentialClassifier
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from sklearn.cross_validation import StratifiedKFold
from sentiment_util import remove_stopwords, load_datasets

def main():
    x, y = load_datasets(["../datasets/sentiment_uci/yelp_labelled.txt"])

    stopwords = set()
    with open('../stopwords.txt', 'r') as f:
        for w in f:
            stopwords.add(w.strip())

    tok = TweetTokenizer()

    x = [remove_stopwords(tok.tokenize(s.lower()), stopwords) for s in x]
    x = np.array(x)

    accumulate = dict()
    folds = 10
    for train_idx, test_idx in StratifiedKFold(y=y, n_folds=folds, shuffle=True):
        train_x, train_y = x[train_idx], y[train_idx]
        test_x, test_y = x[test_idx], y[test_idx]

        train_docs = [(sent, label) for sent, label in zip(train_x, train_y)]
        test_docs = [(sent, label) for sent, label in zip(test_x, test_y)]

        cls = SentimentAnalyzer()

        # train
        words_with_neg = cls.all_words([mark_negation(a) for a in train_x])
        unigram_feats = cls.unigram_word_feats(words_with_neg)
        cls.add_feat_extractor(extract_unigram_feats, unigrams=unigram_feats, handle_negation=True)

        training_set = cls.apply_features(train_docs, labeled=True)

        # train using conditional exponential classifier
        cls.train(ConditionalExponentialClassifier.train, training_set, max_iter=10, trace=0)

        # test & evaluate
        test_set = cls.apply_features(test_docs)

        for key, value in sorted(cls.evaluate(test_set).items()):
            print('\t{0}: {1}'.format(key, value))
            accumulate.setdefault(key, 0.0)
            accumulate[key] += value if value is not None else 0.0

    print("Averages")
    for key, value in sorted(accumulate.items()):
        print('\tAverage {0}: {1}'.format(key, value/folds))

if __name__ == '__main__':
    main()