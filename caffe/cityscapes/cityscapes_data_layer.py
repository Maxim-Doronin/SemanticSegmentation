import caffe

import numpy as np
from PIL import Image

import random

class CityscapesDataLayer(caffe.Layer):

    def setup(self, bottom, top):

        params = eval(self.param_str)
        self.data_root = params['data_root']
        self.split = params['split']
        self.mean = np.array((104.007, 116.669, 122.679), dtype=np.float32)
        if (self.split == 'train'):
            self.eval_list_img = 'eval_list/train.txt'
        else:
            self.eval_list_img = 'eval_list/val.txt'
        self.random = params.get('randomize', True)
        self.seed = params.get('seed', None)

        if len(top) != 2:
            raise Exception("Need to define two tops: data and label.")
        if len(bottom) != 0:
            raise Exception("Do not define a bottom.")

        self.indices_img = open(self.eval_list_img, 'r').read().splitlines()
        self.idx = 0

        if 'train' not in self.split:
            self.random = False

        if self.random:
            random.seed(self.seed)
            self.idx = random.randint(0, len(self.indices_img)-1)


    def reshape(self, bottom, top):
        relpath_to_img = self.indices_img[self.idx].split()[0]
        relpath_to_label = self.indices_img[self.idx].split()[1]
        self.data = self.load_image(relpath_to_img)
        self.label = self.load_label(relpath_to_label)

        top[0].reshape(1, *self.data.shape)
        top[1].reshape(1, *self.label.shape)


    def forward(self, bottom, top):
        # assign output
        top[0].data[...] = self.data
        top[1].data[...] = self.label

        # pick next input
        if self.random:
            self.idx = random.randint(0, len(self.indices_img)-1)
        else:
            self.idx += 1
            if self.idx == len(self.indices_img):
                self.idx = 0


    def backward(self, top, propagate_down, bottom):
        pass


    def load_image(self, idx):
        im = Image.open('{}/{}'.format(self.data_root, idx))
        in_ = np.array(im, dtype=np.float32)
        if len(in_.shape) == 2:
            in_ = in_[np.newaxis,...]
        else:
            in_ = in_[:,:,::-1]
            in_ -= self.mean
            in_ = in_.transpose((2,0,1))
        return in_


    def load_label(self, idx):
        im = Image.open('{}/{}'.format(self.data_root, idx))
        label = np.array(im, dtype=np.uint8)
        if len(label.shape) == 2:
            label = label[np.newaxis,...]
        else:
            label = label.transpose((2,0,1))
        return label


