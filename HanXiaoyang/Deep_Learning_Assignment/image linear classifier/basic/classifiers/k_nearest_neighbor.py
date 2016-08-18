#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np

class KNearestNeighbor:
  """ L2距离下的KNN """

  def __init__(self):
    pass

  def train(self, X, y):
    """
    训练分类器，其实就是把所有的数据记下来

    Input:
    X - A num_train x dimension array where each row is a training point.
    y - A vector of length num_train, where y[i] is the label for X[i, :]
    """
    self.X_train = X
    self.y_train = y
    
  def predict(self, X, k=1, num_loops=0):
    """
    根据记下来的训练数据，比对测试数据判定类别

    Input:
    X - A num_test x dimension array where each row is a test point.
    k - The number of nearest neighbors that vote for predicted label
    num_loops - Determines which method to use to compute distances
                between training points and test points.

    Output:
    y - A vector of length num_test, where y[i] is the predicted label for the
        test point X[i, :].
    """
    if num_loops == 0:
      dists = self.compute_distances_no_loops(X)
    elif num_loops == 1:
      dists = self.compute_distances_one_loop(X)
    elif num_loops == 2:
      dists = self.compute_distances_two_loops(X)
    else:
      raise ValueError('Invalid value %d for num_loops' % num_loops)

    return self.predict_labels(dists, k=k)

  def compute_distances_two_loops(self, X):
    """
    用2冲for循环来计算L2距离

    Input:
    X - An num_test x dimension array where each row is a test point.

    Output:
    dists - A num_test x num_train array where dists[i, j] is the distance
            between the ith test point and the jth training point.
    """
    num_test = X.shape[0]
    num_train = self.X_train.shape[0]
    dists = np.zeros((num_test, num_train))
    for i in xrange(num_test):
      for j in xrange(num_train):
        # 第张测试图片和第j张训练图片之间的距离        
        dists[i, j] = np.sum( (self.X_train[j,:] - X[i,:] )**2 )

    return dists

  def compute_distances_one_loop(self, X):
    """
    Compute the distance between each test point in X and each training point
    in self.X_train using a single loop over the test data.

    Input / Output: Same as compute_distances_two_loops
    """
    num_test = X.shape[0]
    num_train = self.X_train.shape[0]
    dists = np.zeros((num_test, num_train))
    for i in xrange(num_test):
      # dists[i, :] = np.sum((self.X_train - X[i, :])**2, axis=1 )
      train_2 = np.sum( (self.X_train)**2, axis=1 ).T
      test_2  = np.tile( np.sum( (X[i,:])**2 ), [1, num_train])
      test_train = X[i,:].dot(self.X_train.T)
      
      dists[i,:] = train_2 + test_2 - 2 * test_train

    return dists

  def compute_distances_no_loops(self, X):
    """
    向量化/无循环地实现样本间距离计算

    Input / Output: Same as compute_distances_two_loops
    """
    num_test = X.shape[0]
    num_train = self.X_train.shape[0]
    dists = np.zeros((num_test, num_train)) 
    
    # expand the formula and calculate each term respectively
    train_2 = np.tile( np.sum( (self.X_train)**2, axis=1), [num_test, 1])
    test_2  = np.tile( np.sum( (X)**2, axis=1), [num_train, 1]).T
    test_train = X.dot(self.X_train.T)

    dists = train_2 + test_2 - 2*test_train
    return dists

  def predict_labels(self, dists, k=1):
    """
    给定测试集和训练集的样本距离，判定类别

    Input:
    dists - A num_test x num_train array where dists[i, j] gives the distance
            between the ith test point and the jth training point.

    Output:
    y - A vector of length num_test where y[i] is the predicted label for the
        ith test point.
    """
    num_test = dists.shape[0]
    y_pred = np.zeros(num_test)
    for i in xrange(num_test):
      # A list of length k storing the labels of the k nearest neighbors to
      # the ith test point.
      closest_y = []
      closest_idx = np.argsort(dists[i, :])[:k].tolist()
      closest_y = self.y_train[closest_idx]
      
      # count the frequency of those closest labels
      counts = np.bincount(closest_y)

      # return the most frequent item as result
      y_pred[i] = np.argmax(counts)
    return y_pred

