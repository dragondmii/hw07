#!/usr/bin/python

import argparse
import cv2
import sys
import os
import re
import cPickle as pickle
import fnmatch

########################
# module: image_index.py
# Robert Epstein
# A01092594
########################

ap = argparse.ArgumentParser()
ap.add_argument('-imgdir', '--imgdir', required = True, help = 'image directory')
ap.add_argument('-bgr', '--bgr', required = True, help = 'bgr index file to pickle')
ap.add_argument('-hsv', '--hsv', required = True, help = 'hsv index file to pickle')
ap.add_argument('-gsl', '--gsl', required = True, help = 'gsl index file to pickle')
args = vars(ap.parse_args())

def generate_file_names(fnpat, rootdir):
  for path, dirlist, filelist in os.walk(rootdir):
    for file_name in fnmatch.filter(filelist, fnpat):
      print file_name
      yield os.path.join(path, file_name)
  pass


## three index dictionaries
HSV_INDEX = {}
BGR_INDEX = {}
GSL_INDEX = {}

def index_img(imgp):
    try:
        img = cv2.imread(imgp)
        index_bgr(imgp, img)
        index_hsv(imgp, img)
        index_gsl(imgp, img)
        del img
    except Exception, e:
        print(str(e))

# compute the bgr vector for img saved in path imgp and
# index it in BGR_INDEX under imgp.
def index_bgr(imgp, img):
    (B, G, R) = cv2.split(img)
    (h, w, num_channels) = img.shape
    bval = 0;
    gval = 0;
    rval = 0;

    for hight in xrange(h):
      for width in xrange(w):
        bval = bval+B[height][width]
        gval = gval+G[height][width]
        rval = rval+R[height][width]
      output = output + (bval/w, gval/w, rval/w)
    cv2.imshow('name', output)
    cv2.waitKey(0)
    BGR_INDEX[imgp] = output
    pass

# compute the hsv vector for img saved in path imgp and
# index it in HSV_INDEX under imgp.
def index_hsv(imgp, img):
    hsv_image =cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    (H, S, V) = cv2.split(hsv_img)
    (h, w, num_channels) = img.shape
    hval = 0;
    sval = 0;
    vval = 0;

    for hight in xrange(h):
      for width in xrange(w):
        hval = hval+H[height][width]
        sval = sval+S[height][width]
        vval = vval+v[height][width]
      output = output + (hval/w, sval/w, vval/w)
    cv2.imshow('name', output)
    cv2.waitKey(0)
    HSV_INDEX[imgp] = output
    pass

# compute the gsl vector for img saved in path imgp and
# index it in GSL_INDEX under imgp.
def index_gsl(imgp, img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    (G) = cv2.split(gray)
    (h, w, num_channels) = img.shape
    gbval = 0;
    
    for hight in xrange(h):
      for width in xrange(w):
        gval = gval+G[height][width]
      output = output + (bval/w, gval/w, rval/w)
    cv2.imshow('name', output)
    cv2.waitKey(0)
    GSL_INDEX[imgp] = output
  pass

# index image directory imgdir
def index_img_dir(imgdir):
  print(imgdir)
  for imgp in generate_file_names(r'.+\.(jpg|png|JPG)', imgdir):
    print('indexing ' + imgp)
    index_img(imgp)
    print(imgp + ' indexed')

# index and pickle
if __name__ == '__main__':
  index_img_dir(args['imgdir'])
  with open(args['bgr'], 'wb') as bgrfile:
    pickle.dump(BGR_INDEX, bgrfile)
  with open(args['hsv'], 'wb') as hsvfile:
    pickle.dump(HSV_INDEX, hsvfile)
  with open(args['gsl'], 'wb') as gslfile:
    pickle.dump(GSL_INDEX, gslfile)
  print('indexing finished')
    

