import numpy as np
from nltk import TweetTokenizer, accuracy
from nltk.stem.snowball import EnglishStemmer
from sklearn import svm
from sklearn.cross_validation import StratifiedKFold
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import precision_recall_fscore_support

from sentiment_util import load_datasets


def main():
    # x, y = load_dataset("datasets/sentiment_uci/yelp_labelled.txt")
    x, y = load_datasets(["../datasets/sentiment_uci/yelp_labelled.txt"])

    stopwords = set()
    with open('../stopwords.txt', 'r') as f:
        for w in f:
            stopwords.add(w)

    tok = TweetTokenizer()
    stemmer = EnglishStemmer()
    vectorizer = TfidfVectorizer(sublinear_tf=True, use_idf=True, binary=True, preprocessor=stemmer.stem,
                                 tokenizer=tok.tokenize, ngram_range=(1, 2))

    accu_p = np.zeros(shape=(2,))
    accu_r = np.zeros(shape=(2,))
    accu_f = np.zeros(shape=(2,))
    accu_a = 0.0
    folds = 10
    for train_idx, test_idx in StratifiedKFold(y=y, n_folds=folds, shuffle=True):
        train_x, train_y = x[train_idx], y[train_idx]
        test_x, test_y = x[test_idx], y[test_idx]

        cls = svm.LinearSVC(loss='hinge', C=2.0, penalty='l2', class_weight=None)

        # train
        train_x = vectorizer.fit_transform(train_x).toarray()

        cls.fit(train_x, train_y)

        # test
        test_x = vectorizer.transform(test_x).toarray()

        pred_y = cls.predict(test_x)

        # evaluate
        p, r, f, _ = precision_recall_fscore_support(test_y, pred_y)
        a = accuracy_score(test_y, pred_y)
        accu_p += p
        accu_r += r
        accu_f += f
        accu_a += a

        print("Evaluating classifier:")
        print("\tAccuracy: {}".format(a))
        print("\tPrecision[0]: {}".format(p[0]))
        print("\tPrecision[1]: {}".format(p[1]))
        print("\tRecall[0]: {}".format(r[0]))
        print("\tRecall[1]: {}".format(r[1]))
        print("\tF1-score[0]: {}".format(f[0]))
        print("\tF1-score[1]: {}".format(f[1]))

    print("Average evaluation")
    print("\tAccuracy: {}".format(accu_a / folds))
    print("\tPrecision[0]: {}".format(accu_p[0] / folds))
    print("\tPrecision[1]: {}".format(accu_p[1] / folds))
    print("\tRecall[0]: {}".format(accu_r[0] / folds))
    print("\tRecall[1]: {}".format(accu_r[1] / folds))
    print("\tF1-score[0]: {}".format(accu_f[0] / folds))
    print("\tF1-score[1]: {}".format(accu_f[1] / folds))

if __name__ == '__main__':
    main()
