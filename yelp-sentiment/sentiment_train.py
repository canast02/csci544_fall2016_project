import numpy as np
from nltk import TweetTokenizer
from sklearn.cross_validation import StratifiedKFold
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.naive_bayes import GaussianNB


def load_dataset(filename):
    x = []
    y = []
    with open(filename, 'r') as f:
        for s, l in map(lambda line: line.strip().split('\t'), f):
            x.append(s)
            y.append(int(l))

    return np.array(x), np.array(y)


def main():
    x, y = load_dataset("datasets/sentiment_uci/yelp_labelled.txt")

    stopwords = set()
    with open('stopwords.txt', 'r') as f:
        for w in f:
            stopwords.add(w)

    tok = TweetTokenizer()
    vectorizer = TfidfVectorizer(sublinear_tf=True, use_idf=True, binary=True, tokenizer=tok.tokenize, ngram_range=(1, 2))

    accu_sum = 0.0
    folds = 10
    for train_idx, test_idx in StratifiedKFold(y=y, n_folds=folds, shuffle=True):
        train_x, train_y = x[train_idx], y[train_idx]
        test_x, test_y = x[test_idx], y[test_idx]

        # train
        train_x = vectorizer.fit_transform(train_x).toarray()

        pos_tfidf = train_x[train_y == 1]
        neg_tfidf = train_x[train_y == 0]

        pos_probs = (pos_tfidf.sum(axis=0) + 1) / (pos_tfidf.sum() + train_x.shape[1])
        neg_probs = (neg_tfidf.sum(axis=0) + 1) / (neg_tfidf.sum() + train_x.shape[1])

        class_pos_prob = (train_y == 1).sum() / len(train_y)
        class_neg_prob = (train_y == 0).sum() / len(train_y)

        # test
        test_x = vectorizer.transform(test_x).toarray()

        pos_test_x = test_x * pos_probs
        pos_test_x[pos_test_x == 0.0] = 1.0
        pos_test_x = np.log(pos_test_x)

        neg_test_x = test_x * neg_probs
        neg_test_x[neg_test_x == 0.0] = 1.0
        neg_test_x = np.log(neg_test_x)

        sum_pos = np.math.log(class_pos_prob) + pos_test_x.sum(axis=1)
        sum_neg = np.math.log(class_neg_prob) + neg_test_x.sum(axis=1)

        test_arr = np.ndarray(shape=(2, len(test_y)))
        test_arr[0] = sum_neg
        test_arr[1] = sum_pos

        pred_y = test_arr.argmax(axis=0)

        # evaluate
        correct = np.equal(test_y, pred_y).sum()
        accu = correct / len(test_y)

        accu_sum += accu
        print("Accuracy: {}".format(accu))

    avg_accu = accu_sum / folds
    print("Average accuracy: {}".format(avg_accu))

if __name__ == '__main__':
    main()
