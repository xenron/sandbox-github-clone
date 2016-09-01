#!/bin/sh

#
# First upgrade apt-get
#

sudo apt-get -y update
sudo apt-get -y upgrade

#
# Install numpy/scipy/theano requirements
#

sudo apt-get -y install git
sudo apt-get -y install make python-dev python-setuptools libblas-dev \
    gfortran g++ python-pip python-numpy python-scipy liblapack-dev
sudo apt-get -y install libjpeg62-dev libfreetype6 libfreetype6-dev libjpeg8

#
# Install CUDA (note 7.5 did not work for me)
#

wget http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1404/x86_64/cuda-repo-ubuntu1404_6.5-14_amd64.deb
sudo dpkg -i cuda-repo-ubuntu1404_7.5-18_amd64.deb
sudo apt-get update
sudo apt-get install cuda

#
# Install python machine learning frameworks
#