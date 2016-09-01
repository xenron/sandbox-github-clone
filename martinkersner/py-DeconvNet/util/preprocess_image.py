#!/usr/bin/env python
# Martin Kersner, martin@company100.com
# 2016/01/06

import numpy as np

def preprocess_image(img, img_sz):
  # B 104.00698793 G 116.66876762 R 122.67891434
  mean = np.array([104.00698793, 116.66876762, 122.67891434])
  
  I = np.array(img, dtype=np.float32)
  #I = I[:,:,::-1]
  I = I[...,[2,1,0]]
  I_zero_mean = I - mean

  row_pad = img_sz - I_zero_mean.shape[0]
  col_pad = img_sz - I_zero_mean.shape[1]

  im = np.pad(I_zero_mean, ((0,row_pad), (0,col_pad), (0,0)), 'constant', constant_values=(0))
  im = im.transpose((2,0,1))

  return im
