__author__ = 'vesnikos'

import cv2
import gdal
import numpy as np

f_in = "f-in.tiff"
f_out = "f-out.png"


ds = gdal.Open(f_in)
arr = ds.ReadAsArray()

clahe = cv2.createCLAHE(clipLimit=12,tileGridSize=(50,50))
r,g,b,nir = arr

img = np.zeros((6000,8000,3),np.uint8)


img[...,0] = clahe.apply(r)
img[...,1] = clahe.apply(g)
img[...,2] = clahe.apply(b)

cv2.imwrite(f_out,img)