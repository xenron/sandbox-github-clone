#!/usr/bin/env python
# Martin Kersner, martin@company100.com
# 2016/01/05

import os

# dataset
#
# Note for experienced users: the VOC2008-11 test sets are subsets
# of the VOC2012 test set. You don't need to do anything special
# to submit results for VOC2008-11.

VOCopts = {}
VOCopts['dataset'] = 'VOC2012_TEST'

# get devkit directory with forward slashes
devkitroot='./data'

# change this path to point to your copy of the PASCAL VOC data
VOCopts['datadir'] = devkitroot

# change this path to a writable directory for your results
VOCopts['resdir'] = os.path.join(devkitroot, 'results/', VOCopts['dataset'])

# change this path to a writable local directory for the example code
VOCopts['localdir'] = os.path.join(devkitroot, 'local/', VOCopts['dataset'])

# initialize the training set

# VOCopts['trainset'] = 'train' # use train for development
VOCopts['trainset'] = 'trainval' # use train+val for final challenge

# initialize the test set

# VOCopts['testset'] = 'val' # use validation data for development test set
VOCopts['testset'] = 'test' # use test set for final challenge

# initialize main challenge paths

VOCopts['annopath'] = os.path.join(VOCopts['datadir'], VOCopts['dataset'], 'Annotations/{}.xml')
VOCopts['imgpath'] = os.path.join(VOCopts['datadir'], VOCopts['dataset'], 'JPEGImages/{}.jpg')
VOCopts['imgsetpath'] = os.path.join(VOCopts['datadir'], VOCopts['dataset'], 'ImageSets/Main/{}.txt')
VOCopts['clsimgsetpath'] = os.path.join(VOCopts['datadir'], VOCopts['dataset'], 'ImageSets/Main/{}_{}.txt')
VOCopts['clsrespath'] = os.path.join(VOCopts['resdir'], 'Main/{}_cls_', VOCopts['testset'], '_{}.txt')
VOCopts['detrespath'] = os.path.join(VOCopts['resdir'], 'Main/{}_det_', VOCopts['testset'], '_{}.txt')

# initialize segmentation task paths

VOCopts['seg.clsimgpath'] = os.path.join(VOCopts['datadir'], VOCopts['dataset'], 'SegmentationClass/{}.png')
VOCopts['seg.instimgpath'] = os.path.join(VOCopts['datadir'], VOCopts['dataset'], 'SegmentationObject/{}.png')

VOCopts['seg.imgsetpath'] = os.path.join(VOCopts['datadir'], VOCopts['dataset'], 'ImageSets/Segmentation/{}.txt')

VOCopts['seg.clsresdir'] = os.path.join(VOCopts['resdir'], 'Segmentation/{}_{}_cls')
VOCopts['seg.instresdir'] = os.path.join(VOCopts['resdir'], 'Segmentation/{}_{}_inst')
VOCopts['seg.clsrespath'] = os.path.join(VOCopts['seg.clsresdir'], '{}.png')
VOCopts['seg.instrespath'] = os.path.join(VOCopts['seg.instresdir'], '{}.png')

# initialize layout task paths

VOCopts['layout.imgsetpath'] = os.path.join(VOCopts['datadir'], VOCopts['dataset'], 'ImageSets/Layout/{}.txt')
VOCopts['layout.respath'] = os.path.join(VOCopts['resdir'], 'Layout/{}_layout_', VOCopts['testset'], '.xml')

# initialize action task paths

VOCopts['action.imgsetpath'] = os.path.join(VOCopts['datadir'], VOCopts['dataset'], 'ImageSets/Action/{}.txt')
VOCopts['action.clsimgsetpath'] = os.path.join(VOCopts['datadir'], VOCopts['dataset'], 'ImageSets/Action/{}_{}.txt')
VOCopts['action.respath'] = os.path.join(VOCopts['resdir'], 'Action/{}_action_', VOCopts['testset'], '_{}.txt')

# initialize the VOC challenge options

# classes

VOCopts['classes'] = [
    'aeroplane',
    'bicycle',
    'bird',
    'boat',
    'bottle',
    'bus',
    'car',
    'cat',
    'chair',
    'cow',
    'diningtable',
    'dog',
    'horse',
    'motorbike',
    'person',
    'pottedplant',
    'sheep',
    'sofa',
    'train',
    'tvmonitor']

VOCopts['nclasses'] = len(VOCopts['classes'])

# poses

VOCopts['poses'] = [
    'Unspecified',
    'Left',
    'Right',
    'Frontal',
    'Rear']

VOCopts['nposes'] = len(VOCopts['poses'])

# layout parts

VOCopts['parts'] = [
    'head',
    'hand',
    'foot']

VOCopts['nparts'] = len(VOCopts['parts'])

VOCopts['maxparts'] = [1, 2, 2]   # max of each of above parts

# actions

VOCopts['actions'] = [
    'other',             # skip this when training classifiers
    'jumping',
    'phoning',
    'playinginstrument',
    'reading',
    'ridingbike',
    'ridinghorse',
    'running',
    'takingphoto',
    'usingcomputer',
    'walking']

VOCopts['nactions'] = len(VOCopts['actions'])

# overlap threshold

VOCopts['minoverlap'] = 0.5

# annotation cache for evaluation

VOCopts['annocachepath'] = os.path.join(VOCopts['localdir'], '{}_anno.mat')

# options for example implementations

VOCopts['exfdpath'] = os.path.join(VOCopts['localdir'], '{}_fd.mat')
