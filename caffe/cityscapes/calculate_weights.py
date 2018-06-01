import numpy as np
import os
import sys
from PIL import Image

ROOT_FOLDER = '../../data'
SOURCE = 'eval_list'

WIDTH = 0
HEIGHT = 0

def calculate_frequency(root_folder, source, number_of_classes):
  global WIDTH
  global HEIGHT
  freq = {}
  image_count = {}

  for w in range(number_of_classes):
    freq.update({w: 0})
    image_count.update({w: 0})
  
  txtlines = open(os.path.join(SOURCE, 'train.txt'),'r').read().splitlines()
  im = Image.open(os.path.join(ROOT_FOLDER, txtlines[0].split(' ')[1]))
  in_ = np.array(im, dtype=np.uint8)
  height = in_.shape[0]
  HEIGHT = height
  width = in_.shape[1]
  WIDTH = width

  for line in txtlines:
    im = Image.open(os.path.join(ROOT_FOLDER, line.split(' ')[1]))
    in_ = np.array(im, dtype=np.uint8)
    for class_id in range(number_of_classes):
      sum = (in_ == np.array([class_id])).sum()
      freq.update({class_id: freq.get(class_id) + sum})
      if sum > 0:
        image_count.update({class_id: image_count.get(class_id) + 1})

  return freq, image_count


def calculate_weights(freq, image_count):
  weights = {}
  f_class = {}
  for class_id in freq.keys():
    if image_count.get(class_id):
      value = float(freq.get(class_id)) / (image_count.get(class_id) * HEIGHT * WIDTH)
      f_class.update({class_id: value})

  for class_id in freq.keys():
    if f_class.get(class_id):
      weights.update({class_id: float(np.median(f_class.values())) / f_class.get(class_id)})

  return weights


if __name__ == "__main__":
  freq, image_count = calculate_frequency(ROOT_FOLDER, SOURCE, int(sys.argv[1]))
  print calculate_weights(freq, image_count)  