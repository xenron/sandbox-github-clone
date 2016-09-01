#!/usr/bin/env python
# Martin Kersner, martin@company100.com
# 2016/01/08

import numpy as np
from scipy.misc import imresize

def preprocess_image_bb(img, box, img_sz):
  meanImg = np.array([104.00698793, 116.66876762, 122.67891434]) # order = bgr
  
  img = np.array(img, dtype=np.float32)
  crop = img[box[1]:box[3],box[0]:box[2],:] 
  crop = imresize(crop, (img_sz, img_sz), interp='bilinear') # resize cropped image
  crop = crop[...,[2,1,0]] - meanImg # convert color channer rgb->bgr and subtract mean 
  
  preprocessed_img = crop.transpose((2, 0, 1))
  
  return preprocessed_img
