import caffe

import numpy as np
from PIL import Image

import random

class CityscapesDataLayer(caffe.Layer):
    """
    Load (input image, label image) pairs from PASCAL VOC
    one-at-a-time while reshaping the net to preserve dimensions.
    Use this to feed data to a fully convolutional network.
    """

    def setup(self, bottom, top):
        """
        Setup data layer according to parameters:
        - voc_dir: path to PASCAL VOC year dir
        - split: train / val / test
        - mean: tuple of mean values to subtract
        - randomize: load in random order (default: True)
        - seed: seed for randomization (default: None / current time)
        for PASCAL VOC semantic segmentation.
        example
        params = dict(voc_dir="/path/to/PASCAL/VOC2011",
            mean=(104.00698793, 116.66876762, 122.67891434),
            split="val")
        """
        # config
        params = eval(self.param_str)
        self.data_root = params['data_root']
        self.split = params['split']
        if (self.split == 'train'):
            self.eval_list_img = 'eval_list/cityscapes_train_img.txt'
            self.eval_list_label = 'eval_list/cityscapes_train_label.txt'
        else:
            self.eval_list_img = 'eval_list/cityscapes_val_img.txt'
            self.eval_list_label = 'eval_list/cityscapes_val_label.txt'

        self.save_root = 'mc_result/cityscapes/val/test_net/';

        self.mean = np.array(params['mean'])
        self.random = params.get('randomize', True)
        self.seed = params.get('seed', None)

        # two tops: data and label
        if len(top) != 2:
            raise Exception("Need to define two tops: data and label.")
        # data layers have no bottoms
        if len(bottom) != 0:
            raise Exception("Do not define a bottom.")

        # load indices for images and labels
        self.indices_img = open(self.eval_list_img, 'r').read().splitlines()
        self.indices_label = open(self.eval_list_label, 'r').read().splitlines()
        self.idx = 0

        # make eval deterministic
        if 'train' not in self.split:
            self.random = False

        # randomization: seed and pick
        if self.random:
            random.seed(self.seed)
            self.idx = random.randint(0, len(self.indices_img)-1)


    def reshape(self, bottom, top):
        # load image + label image pair
        self.data = self.load_image(self.indices_img[self.idx])
        self.label = self.load_label(self.indices_label[self.idx])
        # reshape tops to fit (leading 1 is for batch dimension)
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
        """
        Load input image and preprocess for Caffe:
        - cast to float
        - switch channels RGB -> BGR
        - subtract mean
        - transpose to channel x height x width order
        """
        im = Image.open('{}/leftImg8bit/{}/{}'.format(self.data_root, self.split,
                                                     idx))
        in_ = np.array(im, dtype=np.float32)
        in_ = in_[:,:,::-1]
        in_ -= self.mean
        in_ = in_.transpose((2,0,1))
        return in_


    def load_label(self, idx):
        """
        Load label image as 1 x height x width integer array of label indices.
        The leading singleton dimension is required by the loss.
        """
        im = Image.open('{}/gtFine/{}/{}'.format(self.data_root, self.split, idx))
        label = np.array(im, dtype=np.uint8)
        label = label[np.newaxis, ...]
        return label


