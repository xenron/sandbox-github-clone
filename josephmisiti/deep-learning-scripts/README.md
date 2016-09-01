
### Introduction

So you are saying to yourself .... "another fucking deep learning installation". And you know what? That is exactly what this fucking is.

The reason this repo exists is because

1. I'm hands on, and learn by doing, not by watching
1. I have been doing a lot of deep learning stuff recently, and like to try
to use the latest packages/operating systems /etc. when I do it
1. I dont give a fuck what you think.

If this doesnt work for you, send me a pull request or submit and issue. It was
tested on UBUNTU 14.04 LTS (I did not use someone's existing AMI)

If you just want the AMI, the public AMI is available: i-XXXXXXX

### Common Questions

#### Does this tutorial assume you already have a GPU running already ?

Yes it does, if you need more info on how to setup a GPU instance on EC2, follow
[this excellent tutorial]()

#### Do you I know if I have a valid GPU for CUDA ?

Simple, execute the following command:

```
lspci | grep -i nvidia
```

#### How do I know if Theano is configured to use my GPUs?

Simple, execute the following command:

```
```

#### Theano is complaining the compiler is not installed, what do I do ?

If you see the following command:

```
ubuntu@ip-1-1-1-1:~$ python -c 'import theano'
ERROR (theano.sandbox.cuda): nvcc compiler not found on $PATH. Check your nvcc installation and try again.
```

If you saw this command you need to find out which version you are and then execute this command, replacing `7.5` with your version:

```
echo -e "\nexport PATH=/usr/local/cuda-7.5/bin:$PATH\n\nexport LD_LIBRARY_PATH=/usr/local/cuda-7.5/lib64" >> .bashrc
```

You can find your versionb y looking at the `cuda` folder in the following directory:

#### Theano is complaining that it can't find my GPU, what do I do?

Did you see the following error:

```
ubuntu@ip-1-1-1-1:~$ python -c 'import theano'
modprobe: ERROR: could not insert 'nvidia_352': Unknown symbol in module, or unknown parameter (see dmesg)
WARNING (theano.sandbox.cuda): CUDA is installed, but device gpu0 is not available  (error: Unable to get the number of gpus available: no CUDA-capable device is detected)
```

This one is pretty easy to solve, but I am not exactly sure why it is happening to you. The fix has to do with version numbers not being comptabile with each other.

First purge your existing `nvidia` drivers:

```
sudo apt-get remove --purge nvidia-*
```

Now try installing new ones:

```
sudo add-apt-repository ppa:xorg-edgers/ppa -y
sudo apt-get update
sudo apt-get install nvidia-352
```

This was taken from [this answer](http://stackoverflow.com/a/32556866)


#### 

https://developer.nvidia.com/cuda-downloads