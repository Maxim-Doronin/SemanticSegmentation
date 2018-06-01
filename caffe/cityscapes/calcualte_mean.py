import os
import numpy as np
from PIL import Image

ROOT_FOLDER = '../../data'
SOURCE = 'eval_list'


def calculate_mean(root_folder, source):
  means = [[],[],[]]

  txtlines = open(os.path.join(source, 'train.txt'),'r').read().splitlines()
  im = Image.open(os.path.join(root_folder, txtlines[0].split(' ')[0]))

  # get width and height of images.
  in_ = np.array(im, dtype=np.uint8)
  height = in_.shape[0]
  width = in_.shape[1]

  for line in txtlines:
    im = Image.open(os.path.join(ROOT_FOLDER, line.split(' ')[0]))
    in_ = np.array(im, dtype=np.uint8)

    for i in range(3):
      means[i].append(np.mean(in_[:,:,i]))
    
  return [np.mean(means[0]), np.mean(means[1]), np.mean(means[2])]


if __name__ == "__main__":
    print calculate_mean(ROOT_FOLDER, SOURCE)


