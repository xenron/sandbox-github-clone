#!/usr/bin/env python

'''
Martin Kersner, m.kernser@gmail.com
2016/08/04

Modified from https://github.com/opencv/opencv/blob/master/samples/python/grabcut.py

Usage:
from GrabCut import *
gc = GrabCut(filename)
gc.run()

Control:
 q -> quits
 n -> update segmentation
 0 -> obvious background
 1 -> obvious foreground
 2 -> probable background
 3 -> probable foreground
 right click mouse -> initial segmentation
 left click mouse  -> detailed segmentation
'''

import numpy as np
import cv2

class GrabCut():
  def __init__(self, filename):
    self.BLUE  = [255,   0,   0]
    self.RED   = [  0,   0, 255]
    self.GREEN = [  0, 255,   0]
    self.BLACK = [  0,   0,   0]
    self.WHITE = [255, 255, 255]

    self.BGD    = {'color': self.BLACK, 'val': 0}
    self.FGD    = {'color': self.WHITE, 'val': 1}
    self.PR_BGD = {'color': self.RED,   'val': 2}
    self.PR_FGD = {'color': self.GREEN, 'val': 3}
    self.value      = self.BGD

    self.rect   = None
    self.radius = 3

    # Flags
    self.brush     = False
    self.rectangle = False
    self.rect_over = False
    self.mask_flag = None

    self.initializate(filename)
    self.create_windows()

  def draw_rectangle(self, x, y):
    cv2.rectangle(self.img, (self.ix, self.iy), (x, y), self.BLUE, 2)

  def create_rectangle(self, x, y):
    return (min(self.ix, x), min(self.iy, y), abs(self.ix-x), abs(self.iy-y))

  def draw_circles(self, x, y):
    '''Draw circle both on displayed image and hidden mask'''
    cv2.circle(self.img,  (x, y), self.radius, self.value['color'], -1)
    cv2.circle(self.mask, (x, y), self.radius, self.value['val'],   -1)

  def on_mouse(self, event, x, y, flags, param):
    # RECTANGLE ############################################################
    # Start
    if event == cv2.EVENT_RBUTTONDOWN:
      self.rectangle = True
      self.ix = x 
      self.iy = y

    # Draw
    elif event == cv2.EVENT_MOUSEMOVE:
      if self.rectangle == True:
        self.img = self.img_backup.copy() # reload displayed image
        self.draw_rectangle(x, y)

    # Finish
    elif event == cv2.EVENT_RBUTTONUP:
      if self.rectangle == True:
        self.rectangle = False
        self.rect_over = True
        self.mask_flag = False
        self.draw_rectangle(x, y)
        self.rect = self.create_rectangle(x, y)

    # BRUSH ################################################################
    # Start
    if event == cv2.EVENT_LBUTTONDOWN:
      if self.rect_over:
        self.brush = True
        self.draw_circles(x, y)

    # Draw
    elif event == cv2.EVENT_MOUSEMOVE:
      if self.brush == True:
        self.draw_circles(x, y)

    # Finish 
    elif event == cv2.EVENT_LBUTTONUP:
      if self.brush == True:
        self.brush = False
        self.draw_circles(x, y)

  def initializate(self, filename):
    self.img = cv2.imread(filename)
    self.img_backup = self.img.copy()
    self.mask = np.zeros(self.img.shape[:2], dtype=np.uint8)
    self.output = np.zeros(self.img.shape, np.uint8)

  def create_windows(self):
    cv2.namedWindow("input")
    cv2.namedWindow("output")
    cv2.setMouseCallback("input", self.on_mouse)

  def grab_cut_wrapper(self, mode):
    bgdmodel = np.zeros((1,65),np.float64)
    fgdmodel = np.zeros((1,65),np.float64)
    cv2.grabCut(self.img_backup, self.mask, self.rect, bgdmodel, fgdmodel, 1, mode)

  def empty_mask(self):
    if np.sum(self.mask) == 0:
      return True
    else:
      return False

  def run(self): 
    while (True):
      cv2.imshow("output", self.output)
      cv2.imshow("input",  self.img)
      k = 0xFF & cv2.waitKey(1)

      if k == ord('q'):
        cv2.destroyAllWindows()
        break
      elif k == ord('0'):
        self.value = self.BGD
      elif k == ord('1'):
        self.value = self.FGD
      elif k == ord('2'):
        self.value = self.PR_BGD
      elif k == ord('3'):
        self.value = self.PR_FGD
      elif k == ord('n'): # segment the image
        if self.mask_flag:
          if not self.empty_mask():
            self.grab_cut_wrapper(cv2.GC_INIT_WITH_MASK)
        else:
          if self.rect:
            self.grab_cut_wrapper(cv2.GC_INIT_WITH_RECT)
            self.mask_flag = True

      self.bitwise_mask = np.where(np.add((self.mask==1),(self.mask==3)), 255, 0).astype(np.uint8) # mask made from obvious foreground and and possible foreground
      self.output = cv2.bitwise_and(self.img_backup, self.img_backup, mask=self.bitwise_mask)
