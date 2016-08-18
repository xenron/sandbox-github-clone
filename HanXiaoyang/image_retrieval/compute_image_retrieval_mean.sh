#!/usr/bin/env sh
# 计算leveldb中存储的训练图片集的均值
# 请预先训练好caffe

/home/work/hanxiaoyang/image_retrieval/caffe/build/tools/compute_image_mean -backend leveldb /home/work/hanxiaoyang/image_retrieval/caffe/examples/image_retrieval_train_leveldb \
  /home/work/hanxiaoyang/image_retrieval/caffe/examples/meilishuo_mean.binaryproto

echo "Compute images mean file Done!"
