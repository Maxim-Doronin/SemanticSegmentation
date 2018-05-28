import os
import numpy as np
from PIL import Image

ROOT_FOLDER = '../../data'
SOURCE = 'eval_list'
freq = {}
image_count = {}
weights = {}

txtlines = open(os.path.join(SOURCE, 'train.txt'),'r').read().splitlines()

im = Image.open(os.path.join(ROOT_FOLDER, txtlines[0].split(' ')[1]))
in_ = np.array(im, dtype=np.uint8)
height = in_.shape[0]
width = in_.shape[1]

for w in range(34):
  freq.update({w: 0})
  image_count.update({w: 0})

count = 0
for line in txtlines:
  count += 1
  im = Image.open(os.path.join(ROOT_FOLDER, line.split(' ')[1]))
  in_ = np.array(im, dtype=np.uint8)
  for class_id in range(34):
    sum = (in_ == np.array([class_id])).sum()
    freq.update({class_id: freq.get(class_id) + sum})
    if sum > 0:
      image_count.update({class_id: image_count.get(class_id) + 1})
  if count % 10 == 0:
    print count

  if count % 100 == 0:
    print freq
    print image_count
    f_class = {}
    for class_id in freq.keys():
      if image_count.get(class_id):
        value = float(freq.get(class_id)) / (image_count.get(class_id) * height * width)
        f_class.update({class_id: value})

    for class_id in freq.keys():
      if f_class.get(class_id):
        weights.update({class_id: float(np.median(f_class.values())) / f_class.get(class_id)})

    print weights

print freq
print image_count
