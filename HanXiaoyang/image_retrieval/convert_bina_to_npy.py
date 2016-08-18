#! /usr/bin/env python
#coding=utf-8

# Authors: Hanxiaoyang <hanxiaoyang.ml@gmail.com>
# convert binary image file to numpy array file

# 代码功能：将caffe生成的图像集均值文件转成python的numpy可读的npy文件
# 作者：寒小阳<hanxiaoyang.ml@gmail.com>

import sys
# change the following path to your compiled caffe python path
# 请先编译caffe代码以及python接口部分，将如下的路径改为编译后的python路径
sys.path.append("/home/work/hanxiaoyang/image_retrieval/caffe/python")
import caffe
import numpy as np


if len(sys.argv) != 3:
	print "Usage: python convert_protomean.py proto.mean out.npy"
	sys.exit()
# creat blob
blob = caffe.proto.caffe_pb2.BlobProto()
# read binary image mean data
data = open( sys.argv[1] , 'rb' ).read()
# transform data and get numpy array
blob.ParseFromString(data)
arr = np.array(caffe.io.blobproto_to_array(blob) )
out = arr[0]
# save numpy format data to npy file
np.save(sys.argv[2] , out)
