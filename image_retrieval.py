#!/usr/bin/python

import argparse
import cv2
import sys
import os
import re
import cPickle as pickle

########################
# module: image_retrieval.py
# Robert Epstein
# A01092594
########################

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--imgpath', required = True, help = 'image path')
ap.add_argument('-bgr', '--bgr', required = True, help = 'bgr index file to unpickle')
ap.add_argument('-hsv', '--hsv', required = True, help = 'hsv index file to unpickle')
ap.add_argument('-gsl', '--gsl', required = True, help = 'gsl index file to unpickle')
args = vars(ap.parse_args())

def mean(v):
  return sum(v)/(len(v)*1.0)

# compute the bgr similarity between
# two bgr index vectors
def bgr_img_sim(img_index_vec1, img_index_vec2):
  b = abs(mean(img_index_vec1[0])-mean(img_index_vec2[0]))
  g = abs(mean(img_index_vec1[1])-mean(img_index_vec2[1]))
  r = abs(mean(img_index_vec1[2])-mean(img_index_vec2[2]))
  yield (b, g, r)
  pass
  
# compute the hsv similarity between
# two hsv index vectors
def hsv_img_sim(img_index_vec1, img_index_vec2):
  h = abs(mean(img_index_vec1[0])-mean(img_index_vec2[0]))
  s = abs(mean(img_index_vec1[1])-mean(img_index_vec2[1]))
  v = abs(mean(img_index_vec1[2])-mean(img_index_vec2[2]))
  yield (h, s, v)
  pass

# compute the hsv similarity between
# two gsl index vectors
def gsl_img_sim(img_index1, img_index2):
  g = abs(mean(img_index_vec1)-mean(img_index_vec2))
  yield (g)
  pass

# index the input image
def index_img(imgp):
    try:
        img = cv2.imread(imgp)
        if img is None:
          print('cannot read ' + imgp)
          return
        rslt = (index_bgr(img), index_hsv(img), index_gsl(img))
        del img
        return rslt
    except Exception, e:
        print(str(e))

# this is very similar to index_bgr in image_index.py except
# you do not have to save the index in BGR_INDEX. This index
# is used to match the indices in the unpickeld BGR_INDEX.
def index_bgr(img):
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
    return output
    pass

# this is very similar to index_hsv in image_index.py except
# you do not have to save the index in HSV_INDEX. This index
# is used to match the indices in the unpickeld HSV_INDEX.
def index_hsv(img):
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
    return output
    pass

# this is very similar to index_gs. in image_index.py except
# you do not have to save the index in GSL_INDEX. This index
# is used to match the indices in the unpickeld GSL_INDEX.
def index_gsl(img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    (G) = cv2.split(gray)
    (h, w, num_channels) = img.shape
    gbval = 0;
    
    for hight in xrange(h):
      for width in xrange(w):
        gval = gval+G[height][width]
      output = output + (bval/w, gval/w, rval/w)
    return output
    pass

# we will unpickle into these global vars below.
BGR_INDEX = None
HSV_INDEX = None
GSL_INDEX = None

# compute the similarities between the bgr
# index vector and all the vectors in the unpickled
# bgr index bgr_index and return the top one.
def compute_bgr_sim(bgr, bgr_index, topn=1):
  holding_list = ()
  for x in xrange(len(bgr_index)):
    holding_list = list(bgr_img_sim(bgr, bgr_index[x]), bgr_index[x])
  sort_things = sorted(holding_list,key = holding_list[0] reverse=True)
  for i in xrange(topn+1):
    yield(sort_things[i][1])
  pass

# compute the similarities between the hsv
# index vector and all the vectors in the unpickled
# hsv index hsv_index and return the top one.
def compute_hsv_sim(hsv, hsv_index, topn=1):
  holding_list = ()
  for x in xrange(len(bgr_index)):
    holding_list = list(hsv_img_sim(hsv, hsv_index[x]), hsv_index[x])
  sort_things = sorted(holding_list,key = holding_list[0] reverse=True)
  for i in xrange(topn+1):
    yield(sort_things[i][1])
  pass

# compute the similarities between the gsl
# index vector and all the vectors in the unpickled
# gsl index gls_index and return the top one.
def compute_gsl_sim(gsl, gsl_index, topn=1):
  holding_list = ()
  for x in xrange(len(gsl_index)):
    holding_list = list(gsl_img_sim(gsl, gsl_index[x]), gsl_index[x])
  sort_things = sorted(holding_list,key = holding_list[0] reverse=True)
  for i in xrange(topn+1):
    yield(sort_things[i][1])
  pass

# unpickle, match, and display
if __name__ == '__main__':
  with open(args['bgr'], 'rb') as bgrfile:
    BGR_INDEX = pickle.load(bgrfile)
  with open(args['hsv'], 'rb') as hsvfile:
    HSV_INDEX = pickle.load(hsvfile)
  with open(args['gsl'], 'rb') as gslfile:
    GSL_INDEX = pickle.load(gslfile)

  bgr, hsv, gsl = index_img(args['imgpath'])
  bgr_matches = compute_bgr_sim(bgr, BGR_INDEX)
  hsv_matches = compute_hsv_sim(hsv, HSV_INDEX)
  gsl_matches = compute_gsl_sim(gsl, GSL_INDEX)

  print bgr_matches
  print hsv_matches
  print gsl_matches

  orig = cv2.imread(args['imgpath'])
  bgr = cv2.imread(bgr_matches[0][0])
  hsv = cv2.imread(hsv_matches[0][0])
  gsl = cv2.imread(hsv_matches[0][0])
  cv2.imshow('Input', orig)
  cv2.imshow('BGR', bgr)
  cv2.imshow('HSV', hsv)
  cv2.imshow('GSL', gsl)
  cv2.waitKey()
  del orig
  del bgr
  del hsv
  del gsl
  cv2.destroyAllWindows()
    

