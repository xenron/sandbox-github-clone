#!/usr/bin/env python

'''
Martin Kersner, m.kersner@gmail.com
2016/08/04

./GrabCut_example.py image.jpg
'''

import os
import sys
from GrabCut import *

def main():
  filename = validate_image(sys.argv)
  gc = GrabCut(filename)
  gc.run()

def validate_image(argv):
  if len(argv) == 2:
    filename = argv[1]

    if not os.path.exists(filename):
      quit("Image path does not exist.")

  else:
    quit("./GrabCut_example.py image.jpg")

  return filename

def quit(msg=None):
  if msg:
    print msg

  exit()

if __name__  == "__main__":
  main()
