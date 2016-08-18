#! /usr/bin/env python
#coding=utf-8

# Authors: Hanxiaoyang <hanxiaoyang.ml@gmail.com>
# use caffe and pre-trained model to compute image feature for image retrieval

# 代码功能：用caffe和预先训练好的卷积神经网络模型，从图片中抽取出图像检索所需的特征，并存储在pkl文件中
# 作者：寒小阳<hanxiaoyang.ml@gmail.com>

import sys
# change the following path to your compiled caffe python path
# 请先编译caffe代码以及python接口部分，将如下的路径改为编译后的python路径
sys.path.append("/home/work/hanxiaoyang/image_retrieval/caffe/python")
import caffe
import numpy as np
import os
from scipy.sparse import csr_matrix
import cPickle
import logging
import datetime

if __name__ == '__main__':
	if len(sys.argv) != 6:
		print "usage: python compute_fea_for_image_retrieval.py [img_name_file] [net_def_prototxt] [trained_net_caffemodel] [image_mean_file] [out_put dir]"
		exit(1)
	#每300张一个batch进行前向计算，拿到feature
	batchsize = 300
	img_file = sys.argv[1]

	logfile = "log_" + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
	logging.basicConfig(filename=logfile, level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
	
	# prototxt神经网络配置文件
	net_def_prototxt = sys.argv[2]
	# 训练好的模型
	trained_net_caffemodel = sys.argv[3]
	# 设定gpu模型，若只有cpu，注释掉这一行
	caffe.set_mode_gpu()
	# 设定cpu模式，若有gpu，请注释掉这一行
	caffe.set_mode_cpu()
	# 通过网络定义文件prototxt和预训练好的模型设定神经网路
	net = caffe.Net(net_def_prototxt, trained_net_caffemodel, caffe.TEST)
	# 图像预处理部分需要transform
	transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
	transformer.set_transpose('data', (2,0,1)) # height*width*channel -> channel*height*width
	# 载入均值文件
	mean_file = sys.argv[4]
	mean_file = np.load(mean_file).mean(1).mean(1)
	transformer.set_mean('data', mean_file) #### subtract mean ####
	transformer.set_raw_scale('data', 255) # pixel value range
	transformer.set_channel_swap('data', (2,1,0)) # RGB -> BGR

	# 设定batchsize
	data_blob_shape = net.blobs['data'].data.shape
	data_blob_shape = list(data_blob_shape)
	net.blobs['data'].reshape(batchsize, data_blob_shape[1], data_blob_shape[2], data_blob_shape[3])
	img_list = []
	tid_list = []
        file_count = 0
	count = 0
	# 设定特征写入文件所在文件夹名
	out_dir = sys.argv[5]
	for line in open(img_file):
		img, tag = line.strip().split(' ')
		tid = img[img.rindex("/")+1:img.rindex(".")]
		try:
			img_list += [caffe.io.load_image("/home/work/hanxiaoyang/pic/"+img)]
			tid_list += [int(tid)]
			count += 1
            file_count += 1
		except:
			continue
		if count == batchsize:
			count = 0
			# 载入batchsize张图片数据
			net.blobs['data'].data[...] = map(lambda x: transformer.preprocess('data',x), img_list)
			# 卷积神经网络前向运算
			net.forward()
			# 获得cf7层4096维的feature
			fc7_fea = net.blobs["fc7"].data[:]
			# 通过fc8_kevin_encode层获得二值检索向量
			fc8_fea = net.blobs["fc8_kevin_encode"].data[:]
			fc8_fea = (fc8_fea>=0.5)*1
			tid_arr = np.array([tid_list]).T
			# numpy存储结果
			result = np.hstack((tid_arr, fc7_fea, fc8_fea))
			img_list = []
			tid_list = []
			#每300张dump到pickle文件中
            if file_count%300 == 0:
				f = open(out_dir+"/"+img_file[-2:]+"_"+str(file_count/300)+".pkl",'wb')
				cPickle.dump(csr_matrix(result),f,-1)
				f.close()
				logging.info(img_file+str(file_count)+"文件已经被存储")
		else:
			continue
	f.close()
	#out = np.packbits(output, axis=-1)
	#print out
