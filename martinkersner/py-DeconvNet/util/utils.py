#!/usr/bin/env python
# Martin Kersner, martin@company100.com
# 2016/01/06

from __future__ import print_function
import os
import sys
import numpy as np
from scipy.misc import imresize

def create_dir(dir_name):
  if not os.path.isdir(dir_name):
    os.makedirs(dir_name)

def newline_decorate(func):
  def func_adder(text):
    text += '\n'
    return func(text)
  return func_adder

def log_inline(*msg):
  print("LOG: ", *msg, end='', file=sys.stderr)

@newline_decorate
def log(*msg):
  log_inline(*msg)

def print_new_line(*msg):
  def func_wrapper(name):
    print('', file=sys.stderr)
  return func_wrapper

def path_join(*path):
  return os.path.join(*path)

def textread(file_name):
  ids = []
  with open(file_name, 'r') as f:
    for line in f:
     ids.append(line.strip()) 

  return ids

def arrresize_ndim(array, new_dims, interp='bilinear'):
  ndims = array.shape[2]
  arr_resized = np.zeros(new_dims, dtype=array.dtype.type)

  for i in range(ndims):
    arr_resized[:,:,i] = imresize(array[:,:,i], new_dims, interp=interp)

  return arr_resized
