import caffe
import surgery, score

import numpy as np
import os
import sys
import cv2
from PIL import Image
from matplotlib.colors import cnames

colors = {
  0: (0, 0, 0),
  1: (255, 0, 0),
  2: (240, 140, 140),
  3: (255, 120, 0),
  4: (240, 201, 166),
  5: (255, 255, 0),
  6: (188, 183, 46),
  7: (144, 255, 0),
  8: (105, 170, 20),
  9: (206, 246, 154),
  10: (77, 233, 143),
  11: (107, 147, 124),
  12: (12, 98, 48),
  13: (0, 255, 228),
  14: (58, 102, 97),
  15: (0, 180, 255),
  16: (108, 124, 131),
  17: (6, 74, 102),
  18: (0, 60, 255),
  19: (18, 40, 111),
  20: (199, 195, 249),
  21: (159, 67, 254),
  22: (99, 1, 199),
  23: (234, 0, 255),
  24: (150, 8, 163),
  25: (240, 158, 247),
  26: (247, 158, 217),
  27: (225, 7, 151),
  28: (143, 36, 106),
  29: (145, 63, 86),
  30: (187, 187, 187)
}

try:
    import setproctitle
    setproctitle.setproctitle(os.path.basename(os.getcwd()))
except:
    pass


weights = '../cityscapes_iter_25000.caffemodel'
caffe.set_mode_gpu()
net = caffe.Net('test.prototxt', caffe.TEST)
net.copy_from(weights)

img = caffe.io.load_image('jena.png')
img = caffe.io.resize( img, (512 , 512 , 3) )
transposed_img = img.transpose((2,0,1))[::-1,:,:]
net.blobs['data'].data[...] = transposed_img
net.forward()

result = net.blobs['softmax'].data[0]
result *= 255
newresult = np.array(result, dtype=np.uint8)
newresult2 = np.array(result, dtype=np.uint8)
for i in range(512):
  for j in range(512):
    m = 0
    idx = 0
    a = []
    for k in range(30):
      a.append(result[k][i][j])
      if result[k][i][j] > m:
        m = result[k][i][j]
        idx = k
    newresult2[0][i][j] = idx
    newresult2[1][i][j] = m
  
img = newresult2[0]
color_img = Image.new('RGB', (512,512))
for i in range(512):
  for j in range(512):
    color_img.putpixel((i,j),colors.get(img[i][j]))

newresult2 *= 7
j = Image.fromarray(newresult2[0])
j.save('jena______' + str(0) + '_.png', "png")
color_img.save('jena_color.png', "png")

result = net.blobs['softmax'].data[0]
result *= 255
newresult = np.array(result, dtype=np.uint8)
for i in range(30):
  j = Image.fromarray(newresult[i])
  j.save('jena' + str(i) + '_.png', "png")