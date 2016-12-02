from sklearn import svm

from nltk import TweetTokenizer
from nltk.stem.snowball import EnglishStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_recall_fscore_support


class YelpSentimentAnalyzer(object):
    def __init__(self):
        super().__init__()
        self._tok = TweetTokenizer()
        self._stemmer = EnglishStemmer()
        self._vectorizer = TfidfVectorizer(sublinear_tf=True, use_idf=True, binary=True,
                                           preprocessor=self._stemmer.stem,
                                           tokenizer=self._tok.tokenize, ngram_range=(1, 2))
        self._cls = svm.LinearSVC(loss='hinge', C=2.0, penalty='l2', class_weight=None)

    def fit(self, X, y):
        X = self._vectorizer.fit_transform(X).toarray()
        self._cls.fit(X, y)

        return self

    def predict(self, X):
        X = self._vectorizer.transform(X).toarray()

        return self._cls.predict(X)

    @staticmethod
    def evaluate(true_y, pred_y):
        p, r, f, _ = precision_recall_fscore_support(true_y, pred_y)
        a = accuracy_score(true_y, pred_y)

        return a, p, r, f
