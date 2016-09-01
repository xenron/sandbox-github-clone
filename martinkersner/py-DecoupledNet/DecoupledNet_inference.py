#!/usr/bin/env python
# Martin Kersner, martin@company100.com
# 2016/01/12

import time

import caffe
import scipy.io
import numpy as np

from skimage.io import imread, imsave
from skimage.color import label2rgb
from skimage import img_as_ubyte

from util.preprocess_image import *
from util.utils import *
from util.init_VOC2012_TEST import *

def DecoupledNet_inference(config):
  ## start DecoupledNet inference
  log('Start of DecoupledNet inference [{}]'.format(config['model_name']))
  
  ## initialization
  cmap = scipy.io.loadmat(config['cmap'])['cmap']
  
  ## initialize caffe
  log('Initializing caffe')
  caffe.set_mode_gpu()
  caffe.set_device(config['gpuNum'])
  net = caffe.Net(config['Path.CNN.model_proto'], config['Path.CNN.model_data'], caffe.TEST)
  log('Initialization of caffe complete')
  
  ## initialize paths
  save_res_dir = path_join(config['save_root'], config['model_name'])
  save_res_path = path_join(save_res_dir, '{}.png')
  
  ## create directory
  if config['write_file']:
    create_dir(save_res_dir)
  
  log('Start generating result')
  log('Caffe model: {}'.format(config['Path.CNN.model_proto']))
  log('Caffe weight: {}'.format(config['Path.CNN.model_data']))
  
  ## read VOC2012 TEST image set
  ids = textread(VOCopts['seg.imgsetpath'].format(config['imageset']))

  for i in range(len(ids)):
    log_inline('{}/{} [{}]... '.format(i, len(ids), ids[i]))
    start = time.clock()
      
    # read image
    I = img_as_ubyte(imread(VOCopts['imgpath'].format(ids[i])))
      
    im_sz = max(I.shape[0], I.shape[1])
    offset = ((0, im_sz-I.shape[0]), (0, im_sz-I.shape[1]), (0, 0))
    caffe_im = np.pad(I, offset, 'constant', constant_values=(0))
    caffe_im = preprocess_image(caffe_im, config['im_sz'])
    label = np.zeros((config['num_classes'],1,1))

    net.blobs['data'].reshape(1, *caffe_im.shape)
    net.blobs['data'].data[...] = caffe_im 
    net.blobs['cls-score-masked'].reshape(1, *label.shape)
    net.blobs['cls-score-masked'].data[...] = label 
    net.forward()

    cls_score = net.blobs['cls-score-sigmoid'].data[0]
          
    score_map = np.zeros((config['im_sz'], config['im_sz'], config['num_classes']+1)) # N classes + background
      
    ## compute bkg prob
    label = cls_score * (cls_score > config['thres'])

    net.blobs['cls-score-masked'].reshape(1, *label.shape)
    net.blobs['cls-score-masked'].data[...] = label 
    net.forward()

    cls_score = net.blobs['cls-score-sigmoid'].data[0]
    seg_score = net.blobs['seg-score'].data[0].transpose((1,2,0))
            
    softmax_score = softmax(seg_score)
    score_map[:,:,0] = softmax_score[:,:,0]
          
    detected_classes = np.where(cls_score > config['thres'])[0]

    for j in detected_classes:
      label = np.zeros((config['num_classes'],1,1))
      label[j] = cls_score[j]
      net.blobs['cls-score-masked'].reshape(1, *label.shape)
      net.blobs['cls-score-masked'].data[...] = label
      net.forward()
      seg_score = net.blobs['seg-score'].data[0].transpose((1,2,0))
      
      softmax_score = softmax(seg_score)
      score_map[:,:,j+1] = softmax_score[:,:,1]
      
    cidx = np.hstack((0, detected_classes+1))
    score_map[:,:,cidx] += np.sum(score_map, axis=2)[:,:,None] <= 0 # TODO what is it good for?

    norm_score_map = score_map / np.sum(score_map, axis=2)[:,:,None]
    resize_score_map = arrresize_ndim(norm_score_map, (im_sz, im_sz, config['num_classes']+1), 'bilinear') # N classes + background
    cropped_score_map = resize_score_map[0:I.shape[0], 0:I.shape[1], :]
    segmask = np.argmax(cropped_score_map, axis=2)
                  
    if config['write_file']:
      imsave(save_res_path.format(ids[i]), label2rgb(segmask, colors=cmap))

    log_basic('{}s\n'.format(time.clock() - start))

def softmax(seg_score):
  softmax_score = np.exp(seg_score - np.amax(seg_score, axis=2)[:,:,None])
  softmax_score = softmax_score / np.sum(softmax_score, axis=2)[:,:,None]

  return softmax_score
