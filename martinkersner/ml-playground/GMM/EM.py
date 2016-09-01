#!/usr/binb/env python
# Martin Kersner, m.kersner@gmail.com
# 2016/08/08

import numpy as np
import matplotlib.pyplot as plt
from sklearn import mixture
from matplotlib.colors import LogNorm

np.random.seed(0)

def main():
    data = generate_data()
    clf = train_data(data)
    model_details(clf)
    plot_data(data, clf)

def generate_data():
    data = np.vstack([  shift(generate_gaussian(), offset=[10, 10]), \
                        stretch(generate_gaussian()), \
                        shift(stretch(generate_gaussian(), C=[[1.5, 0.4],[1.9, 1.1]]), offset=[-10, 10]) \
                    ])

    return data

def shift(data, offset=[0, 0]):
    return data + np.array(offset)

def stretch(data, C=[[0.0, 0.7], [8.5, 1.0]]):
    return np.dot(data, np.array(C))

def generate_gaussian(n_samples=300, n_dims=2):
    return np.random.randn(n_samples, n_dims)

def train_data(data):
    clf = mixture.GMM(n_components=3, covariance_type='full', verbose=1)
    clf.fit(data)
    print_model_detail("AIC", clf.aic(data))
    print_model_detail("BIC", clf.bic(data))

    return clf

def model_details(clf):
    print_model_detail("Weights", clf.weights_)
    print_model_detail("Means", clf.means_)
    print_model_detail("Covariances", clf.covars_)
    print_model_detail("Converged", clf.converged_)

    ax = plt.axes()
    for i in range(0, len(clf.covars_)):
        draw_arrow(ax, clf.means_[i], clf.covars_[i])


def print_model_detail(name, detail):
    print "{}: \n{}\n".format(name, detail)

def draw_arrow(ax, mean, covar):
    '''
    Directions of the arrow correspond to the eigenvector of covariance matrix and their length to the square root of the eigenvalues.
    '''
    x_0 = mean[0]
    y_0 = mean[1]
    vals, vecs = np.linalg.eig(covar)
    sqrt_vals = np.sqrt(vals)
    fc = ec = "aqua"

    ax.arrow(x_0, y_0, vecs[0, 0]*sqrt_vals[0], vecs[1, 0]*sqrt_vals[0], head_width=0.05, head_length=0.1, fc=fc, ec=ec)
    ax.arrow(x_0, y_0, vecs[0, 1]*sqrt_vals[1], vecs[1, 1]*sqrt_vals[1], head_width=0.05, head_length=0.1, fc=fc, ec=ec)

def plot_data(data, clf):
    min_x = np.min(data[:, 0])
    min_y = np.min(data[:, 1])
    max_x = np.max(data[:, 0])
    max_y = np.max(data[:, 1])

    x = np.linspace(min_x, max_x)
    y = np.linspace(min_y, max_y)

    X, Y = np.meshgrid(x, y)
    XX = np.array([X.ravel(), Y.ravel()]).T

    Z = -clf.score_samples(XX)[0]
    Z = Z.reshape(X.shape)

    plt.contour(X, Y, Z, norm=LogNorm(vmin=1.0, vmax=500.0), levels=np.logspace(0, 2, 20))
    plt.scatter(data[:, 0], data[:, 1], 1.0)

    plt.axis('equal') # plots graph with equal axis ratio
    plt.show()

if __name__ == "__main__":
    main()
