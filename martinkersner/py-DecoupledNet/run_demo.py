#!/usr/bin/env python
# Martin Kersner, martin@company100.com
# 2016/01/12

from util.utils import path_join
from DecoupledNet_inference import DecoupledNet_inference

def main():
  # 'Full', '25', '10', '5'
  annotations = 'Full'
  
  config = {}
  config['imageset'] = 'test'
  config['cmap']= './voc_gt_cmap.mat'
  config['gpuNum'] = 0
  config['Path.CNN.caffe_root'] = './caffe'
  config['save_root'] = './results'

  ## configuration
  config['write_file'] = 1
  config['thres'] = 0.5
  config['im_sz'] = 320
  config['num_classes'] = 20

  if annotations == 'Full':
    ## DecoupledNet Full annotations
    config['model_name'] = 'DecoupledNet_Full_anno';
    config['Path.CNN.script_path'] = './DecoupledNet_Full_anno';
    config['Path.CNN.model_data'] = path_join(config['Path.CNN.script_path'],
                                    'DecoupledNet_Full_anno_inference.caffemodel')
    config['Path.CNN.model_proto'] = path_join(config['Path.CNN.script_path'], 
                                     'DecoupledNet_Full_anno_inference_deploy.prototxt')

  elif annotations == '25':
    ## DecoupledNet 25 annotations
    config['model_name'] = 'DecoupledNet_25_anno'
    config['Path.CNN.script_path'] = './DecoupledNet_25_anno'
    config['Path.CNN.model_data'] = path_join(config['Path.CNN.script_path'], 
                                    'DecoupledNet_25_anno_inference.caffemodel')
    config['Path.CNN.model_proto'] = path_join(config['Path.CNN.script_path'], 
                                     'DecoupledNet_25_anno_inference_deploy.prototxt')
    
  elif annotations == '10':
    ## DecoupledNet 10 annotations
    config['model_name'] = 'DecoupledNet_10_anno'
    config['Path.CNN.script_path'] = './DecoupledNet_10_anno'
    config['Path.CNN.model_data'] = path_join(config['Path.CNN.script_path'], 
                                    'DecoupledNet_10_anno_inference.caffemodel')
    config['Path.CNN.model_proto'] = path_join(config['Path.CNN.script_path'], 
                                     'DecoupledNet_10_anno_inference_deploy.prototxt')
    
  elif annotations == '5':
    ## DecoupledNet 5 annotations
    config['model_name'] = 'DecoupledNet_5_anno'
    config['Path.CNN.script_path'] = './DecoupledNet_5_anno'
    config['Path.CNN.model_data'] = path_join(config['Path.CNN.script_path'], 
                                    'DecoupledNet_5_anno_inference.caffemodel')
    config['Path.CNN.model_proto'] = path_join(config['Path.CNN.script_path'], 
                                     'DecoupledNet_5_anno_inference_deploy.prototxt')
    
  else:
    print "You have to specify the number of employed annotations."
    exit()
  
  DecoupledNet_inference(config)

if __name__ == '__main__':
  main()
