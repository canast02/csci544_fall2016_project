import numpy as np


def load_datasets(filenames):
    x = None
    y = None
    for filename in filenames:
        a, b = load_dataset(filename)
        if x is None:
            x = a
            y = b
        else:
            x = np.concatenate((x, a), axis=0)
            y = np.concatenate((y, b), axis=0)

    return x, y


def load_dataset(filename):
    x = []
    y = []
    with open(filename, 'r') as f:
        for s, l in map(lambda line: line.strip().split('\t'), f):
            x.append(s)
            y.append(int(l))

    return np.array(x), np.array(y)


def remove_stopwords(sentence, stopwords):
    return list(filter(lambda x: x.lower() not in stopwords, sentence))
