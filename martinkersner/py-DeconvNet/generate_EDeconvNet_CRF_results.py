#!/usr/bin/env python
# Martin Kersner, martin@company100.com
# 2016/01/06

import time

import caffe
import numpy as np

import scipy.io
#from scipy.misc import imresize

from skimage.io import imread, imsave
from skimage.color import label2rgb
from skimage import img_as_ubyte

from util.preprocess_image_bb import *
from util.utils import *

def generate_EDeconvNet_CRF_results(config, VOCopts):
  log('start generating EDeconvNet+CRF results');
  
  ## initialization
  cmap = scipy.io.loadmat(config['cmap'])['cmap']
  
  ## initialize caffe
  log('initializing caffe..');
  caffe.set_mode_gpu()
  caffe.set_device(config['gpuNum'])
  net = caffe.Net(config['Path.CNN.model_proto'], config['Path.CNN.model_data'], caffe.TEST)
  log('done');
  
  ## initialize paths
  save_res_dir = path_join(config['save_root'], 'EDeconvNet_CRF')
  save_res_path = path_join(save_res_dir, '{}.png')
  edgebox_cache_path = path_join(config['edgebox_cache_dir'], '{}.mat')
  
  fcn_score_dir = path_join(config['fcn_score_dir'], 'scores')
  fcn_score_path = path_join(fcn_score_dir, '{}.npy')
  
  ## create directory
  if config['write_file']:
    create_dir(save_res_dir)
  
  log('start generating result')
  log('caffe model: {}'.format(config['Path.CNN.model_proto']))
  log('caffe weight: {}'.format(config['Path.CNN.model_data']))
  
  
  ## read VOC2012 TEST image set
  ids = textread(VOCopts['seg.imgsetpath'].format(config['imageset']))
  
  for i in range(1):
  #for i in range(len(ids)):
    log_inline('progress: {}/{} [{}]...'.format(i, len(ids), ids[i]))
    start = time.clock()
      
    # read image
    I = img_as_ubyte(imread(VOCopts['imgpath'].format(ids[i]))) # TODO does load correctly?
      
    result_base    = np.zeros((I.shape[0], I.shape[1]), dtype=np.uint8) 
    prob_base      = np.zeros((I.shape[0], I.shape[1], 21));
    cnt_base       = np.zeros((I.shape[0], I.shape[1]), dtype=np.uint8) 
    norm_prob_base = np.zeros((I.shape[0], I.shape[1], 21));
          
    # padding for easy cropping    
    pad_offset_col = I.shape[0]
    pad_offset_row = I.shape[1]
      
    # pad every images(I, cls_seg, inst_seg...) to make cropping easy
    offset_2d = ((pad_offset_row,pad_offset_row), (pad_offset_col,pad_offset_col))
    offset_3d = ((pad_offset_row,pad_offset_row), (pad_offset_col,pad_offset_col), (0, 0))
    padded_I = np.pad(I, offset_3d, 'constant', constant_values=(0))
    padded_result_base = np.pad(result_base, offset_2d, 'constant', constant_values=(0))
    padded_prob_base = np.pad(prob_base, offset_3d, 'constant', constant_values=(0))
    padded_cnt_base = np.pad(cnt_base, offset_2d, 'constant', constant_values=(0))
    norm_padded_prob_base = np.pad(norm_prob_base, offset_3d, 'constant', constant_values=(0))
    norm_padded_prob_base[:,:,1] = np.spacing(1) # Equivalent to Matlab's eps?
          
    # TODO refactor!
    #padded_frame_255 = 255-padarray(uint8(ones(size(I,1),size(I,2))*255),[pad_offset_row, pad_offset_col]);
    padded_frame_255 = 255-np.pad((np.ones((I.shape[0], I.shape[1]), dtype=np.uint8)*255), offset_2d, 'constant', constant_values=(0))
      
    padded_result_base = padded_result_base + padded_frame_255
  
    ## load extended bounding box
    cache = scipy.io.loadmat(edgebox_cache_path.format(ids[i])) # boxes_padded
    boxes_padded = cache['boxes_padded'].astype(np.uint16)
      
    numBoxes = boxes_padded.shape[0]    
    cnt_process = 1
    for bidx in range(numBoxes):
      box = boxes_padded[bidx, :]
      box_wd = box[2]-box[0]
      box_ht = box[3]-box[1]
          
      if min(box_wd, box_ht) < 112:
        continue
          
      input_data = preprocess_image_bb(padded_I, boxes_padded[bidx, :], config['im_sz'])
      net.blobs['data'].reshape(1, *input_data.shape)
      net.blobs['data'].data[...] = input_data 
      net.forward()
      cnn_output = net.blobs['seg-score'].data[0]
          
      segImg = cnn_output.transpose((1,2,0))
      segImg = arrresize_ndim(segImg, (box_ht, box_wd, 21), 'bilinear')
          
      # accumulate prediction result
      cropped_prob_base = padded_prob_base[box[1]:box[3], box[0]:box[2], :]
      padded_prob_base[box[1]:box[3], box[0]:box[2], :] = np.maximum(cropped_prob_base, segImg)
          
      if (cnt_process % 10) == 0:
        log(' {}'.format(cnt_process)) # TODO prograss bar class
        
      if cnt_process >= config['max_proposal_num']:
        break;
          
      cnt_process = cnt_process + 1;

    ## save DeconvNet prediction score
    deconv_score = padded_prob_base[pad_offset_row:pad_offset_row+I.shape[0], 
                                    pad_offset_col:pad_offset_col+I.shape[1],
                                    :]
      
    ## load fcn-8s score
    fcn_score = np.load(fcn_score_path.format(ids[i]))
      
    ## ensemble
    zero_mask = np.zeros_like(fcn_score)
    fcn_score = np.maximum(zero_mask, fcn_score)
          
    ens_score = np.multiply(deconv_score, fcn_score)
    ens_segscore = np.amax(ens_score, axis=2)
    ens_segmask = np.argmax(ens_score, axis=2)

    ## densecrf
    log('[densecrf.. ');
    prob_map = np.exp(ens_score-ens_segscore[:,:,None])
    prob_map = prob_map / np.sum(prob_map, axis=2)[:,:,None]
    unary = -np.log(prob_map) # TODO check!! divide by zero encountered in log
  
    #D = Densecrf(I,single(unary));
    
    # Some settings.
    #D.gaussian_x_stddev = 3;
    #D.gaussian_y_stddev = 3;
    #D.gaussian_weight = 3; 
    #
    #D.bilateral_x_stddev = 20;
    #D.bilateral_y_stddev = 20;
    #D.bilateral_r_stddev = 3;
    #D.bilateral_g_stddev = 3;
    #D.bilateral_b_stddev = 3;
    #D.bilateral_weight = 5;     
    #
    #D.iterations = 10;
    #
    #D.mean_field;
    #segmask = D.segmentation;
    #resulting_seg = uint8(segmask-1);    
    log('done] ');
      
    ## save or display result
    if config['write_file']:
      imsave(save_res_path.format(ids[i]), label2rgb(resulting_seg, colors=cmap))
  
    end = time.clock()
    log(' done [{:f}]'.format(end))
