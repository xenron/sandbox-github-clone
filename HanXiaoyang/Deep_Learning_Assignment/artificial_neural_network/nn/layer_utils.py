#!/usr/bin/env python
# -*- coding: utf-8 -*-
from nn.layers import *
from nn.fast_layers import *

def conv_relu_forward(x, w, b, conv_param):
  """
  把卷积和随后的ReLU激活直接整合在一层里面了

  输入:
  - x: 卷积层的输入
  - w, b, conv_param: 卷积层的权重和参数
  
  结果是一个元组:
  - out: ReLU输出的结果
  - cache: 反向传播需要用到的内容存储的结构体
  """
  a, conv_cache = conv_forward_fast(x, w, b, conv_param)
  out, relu_cache = relu_forward(a)
  cache = (conv_cache, relu_cache)
  return out, cache


def conv_relu_backward(dout, cache):
  """
  卷积-ReLU激活层的反向传播
  """
  conv_cache, relu_cache = cache
  da = relu_backward(dout, relu_cache)
  dx, dw, db = conv_backward_fast(da, conv_cache)
  return dx, dw, db


def conv_relu_pool_forward(x, w, b, conv_param, pool_param):
  """
  把卷积，ReLU激活和池化是现在一层里

  输入:
  - x: 卷积层的输入
  - w, b, conv_param: 卷积层的权重和参数
  - pool_param: 池化层的参数

  结果是一个元组:
  - out: 池化之后输出的结果
  - cache: 反向传播需要用到的内容存储的结构体
  """
  a, conv_cache = conv_forward_fast(x, w, b, conv_param)
  s, relu_cache = relu_forward(a)
  out, pool_cache = max_pool_forward_fast(s, pool_param)
  cache = (conv_cache, relu_cache, pool_cache)
  return out, cache


def conv_relu_pool_backward(dout, cache):
  """
  卷积-relu-池化的反向传播实现
  """
  conv_cache, relu_cache, pool_cache = cache
  ds = max_pool_backward_fast(dout, pool_cache)
  da = relu_backward(ds, relu_cache)
  dx, dw, db = conv_backward_fast(da, conv_cache)
  return dx, dw, db


def affine_relu_forward(x, w, b):
  """
  全连接后接ReLU实现在一层
  
  输入:
  - x: 全连接层的输入
  - w, b: 全连接层的权重和参数
  
  结果是一个元组:
  - out: ReLU之后输出的结果
  - cache: 反向传播需要用到的内容存储的结构体
  """
  a, fc_cache = affine_forward(x, w, b)
  out, relu_cache = relu_forward(a)
  cache = (fc_cache, relu_cache)
  return out, cache


def affine_relu_backward(dout, cache):
  """
  上面实现的层级结构的反向传播
  """
  fc_cache, relu_cache = cache
  da = relu_backward(dout, relu_cache)
  dx, dw, db = affine_backward(da, fc_cache)
  return dx, dw, db
