#!/usr/bin/env python
# Martin Kersner, martin@company100.com
# 2016/01/06

import time

import caffe
import scipy.io

from skimage.io import imread, imsave
from skimage.color import label2rgb
from skimage import img_as_ubyte
#from PIL import Image

from util.preprocess_image import *
from util.utils import *

def cache_FCN8s_results(config, VOCopts):
  log('start caching FCN-8s results and score')
  
  ## initialization
  cmap = scipy.io.loadmat(config['cmap'])['cmap']

  ## initialize caffe
  log('initializing caffe..')
  caffe.set_mode_gpu()
  caffe.set_device(config['gpuNum'])
  net = caffe.Net(config['Path.CNN.model_proto'], config['Path.CNN.model_data'], caffe.TEST)
  log('done')
  
  ## initialize paths
  save_res_dir = path_join(config['save_root'], 'FCN8s/results')
  save_res_path = path_join(save_res_dir, '{}.png')
  save_score_dir = path_join(config['save_root'], 'FCN8s/scores')
  save_score_path = path_join(save_score_dir, '{}.npy')
  
  ## create directory
  if config['write_file']:
    create_dir(save_res_dir)
    create_dir(save_score_dir)
  
  ## load image set
  ids = textread(VOCopts['seg.imgsetpath'].format(config['imageset']))
  
  for i in range(1):
  #for i in range(len(ids)):
      log_inline('progress: {}/{} [{}]...'.format(i, len(ids), ids[i]))
      start = time.clock()
  
      # read image
      I = img_as_ubyte(imread(VOCopts['imgpath'].format(ids[i]))) # TODO does load correctly?
      #I = Image.open(VOCopts['imgpath'].format(ids[i]))
      input_data = preprocess_image(I, config['im_sz']) 

      net.blobs['data'].reshape(1, *input_data.shape)
      net.blobs['data'].data[...] = input_data 
      net.forward()
      cnn_output = net.blobs['upscore'].data[0]

      tr_result = cnn_output.transpose((1,2,0))
      score = tr_result[0:I.shape[0], 0:I.shape[1], :]
      result_seg = np.argmax(score, axis=2)
      #result_seg -= 1 # TODO necessary?
      
      if config['write_file']:
        imsave(save_res_path.format(ids[i]), label2rgb(result_seg, colors=cmap))
        np.save(save_score_path.format(ids[i]), score)

      end = time.clock()
      print str(end - start) + " s"
