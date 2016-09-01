#!/usr/bin/env python
# Martin Kersner, m.kersner@gmail.com

from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris

def main():
    X, y, target_names = load_dataset()
    clf = LogisticRegression()

    #overfit(clf, X, y)

def load_dataset():
    iris = load_iris()
    X = iris["data"]
    y = iris["target"]
    target_names = iris["target_names"]

    return X, y, target_names

def overfit(clf, X, y):
    clf.fit(X, y)
    print clf.score(X, y)

if __name__ == "__main__":
    main()
