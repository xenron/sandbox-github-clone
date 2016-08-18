#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

def init_two_layer_model(input_size, hidden_size, output_size):
  """
  为2层全连接的网络初始化权重和偏移量。网络的输入是D维的，隐层有H个“神经元”，最后分类的类别数为C
  权重初始化为很小的数字，同时偏移量全都初始化为0

  输入:
  - input_size: 输入数据维度D
  - hidden_size: 隐层节点个数H
  - ouput_size: 分类类别数C

  返回:
  一个叫model的python dict，包含下面key，对应的value是numpy数组:
  - W1: First layer weights; has shape (D, H)
  - b1: First layer biases; has shape (H,)
  - W2: Second layer weights; has shape (H, C)
  - b2: Second layer biases; has shape (C,)
  """
  # initialize a model
  model = {}
  # model['W1'] = 0.00001 * np.random.randn(input_size, hidden_size)
  model['W1'] = np.random.randn(input_size, hidden_size) * np.sqrt(2.0 / (input_size * hidden_size) )
  model['b1'] = np.zeros(hidden_size)
  # model['W2'] = 0.00001 * np.random.randn(hidden_size, output_size)
  model['W2'] = np.random.randn(hidden_size, output_size) * np.sqrt(2.0 / (hidden_size * output_size) )
  model['b2'] = np.zeros(output_size)
  return model

def two_layer_net(X, model, y=None, reg=0.0, verbose=False):
  """
  对2层全连接的神经网络计算损失和梯度。
  输入维度为D, 隐层维度为H, 分类类别数为C，我们用的softmax分类器交叉熵损失，加了L2正则化项
  另外这种多层的感知器，需要ReLU这样的激活函数

  总体的结构大概是这样的:

  输入 - 全连接 - ReLU激活 - 全连接 - softmax

  第二个全连接层输出的就是每个类别的得分

  Inputs:
  - X: Input data of shape (N, D). Each X[i] is a training sample.
  - model: Dictionary mapping parameter names to arrays of parameter values.
    It should contain the following:
    - W1: First layer weights; has shape (D, H)
    - b1: First layer biases; has shape (H,)
    - W2: Second layer weights; has shape (H, C)
    - b2: Second layer biases; has shape (C,)
  - y: Vector of training labels. y[i] is the label for X[i], and each y[i] is
    an integer in the range 0 <= y[i] < C. This parameter is optional; if it
    is not passed then we only return scores, and if it is passed then we
    instead return the loss and gradients.
  - reg: Regularization strength.

  Returns:
  如果y没有给定的话， 返回维度为N x C的矩阵，其中第[i, c]个元素是样本X[i]在类别c上的得分

  如果y给定了，会返回下面这样的一个元组:
  - loss: 当前训练batch上的损失（包含正则化项损失）
  - grads: 对应模型参数(字典)的参数梯度
  """

  # unpack variables from the model dictionary
  W1,b1,W2,b2 = model['W1'], model['b1'], model['W2'], model['b2']
  N, D = X.shape

  # 要开始做前向运算了
  scores = None
  
  # ReLU激活层
  hidden_activation = np.maximum( X.dot(W1) + b1, 0)

  if verbose: print "Layer 1 result shape: " + str(hidden_activation.shape)

  # Softmax之前的得分
  scores = hidden_activation.dot(W2) + b2

  if verbose: print "Layer 2 result shape: " + str(scores.shape)
  
  # 没给y的话，把score返回去就算完事了
  if y is None:
    return scores

  # 要开始计算损失/loss啦
  loss = 0

  # 计算tricks(保证运算稳定性)，先减去最大的得分
  scores = scores - np.expand_dims( np.amax( scores, axis=1 ), axis=1)

  exp_scores = np.exp(scores)

  probs = exp_scores / np.sum( exp_scores, axis=1 , keepdims=True)

  # 交叉熵损失
  loss = np.sum(- scores[range(len(y)), y] + np.log( np.sum( exp_scores, axis=1) )) / N

  # L2正则化项
  loss += 0.5 * reg * ( np.sum(W1 ** 2) + np.sum(W2 ** 2) )
  
  # 要开始计算梯度啦
  grads = {}

  # 计算差值
  delta_scores = probs
  delta_scores[range(N), y] -= 1
  delta_scores /= N

  # Softmax层的反向传播
  grads['W2'] = hidden_activation.T.dot(delta_scores)
  grads['b2'] = np.sum( delta_scores, axis=0 )

  # ReLU层的反向传播
  delta_hidden = delta_scores.dot(W2.T)
  
  # 分段函数求导，所以小于0的input是不回传的
  delta_hidden[hidden_activation <= 0] = 0

  grads['W1'] = X.T.dot(delta_hidden)
  grads['b1'] = np.sum(delta_hidden, axis=0 )

  # 正则化部分的梯度
  grads['W2'] += reg * W2
  grads['W1'] += reg * W1


  return loss, grads

