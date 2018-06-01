import caffe
import random
import cv2
import numpy as np
from PIL import Image
import os
import sys

class CityscapesDataLayer(caffe.Layer):

    def get_param(self):

        param = eval(self.param_str)
        self.split = param['split']
        self.source = param['source']
        self.root_folder = param['root_folder']
        self.batch_size = param['batch_size']
        #shuffle each epoch
        if 'shuffle' in param.keys():
            self.shuffle = param['shuffle']
        else:
            self.shuffle = False
        #mean value
        if 'mean_value' in param.keys():
            self.mean_value = param['mean_value']
        else:
            self.mean_value = ()
        #new height
        if 'new_height' in param.keys():
            self.new_height = param['new_height']
        else:
            self.new_height = 0
        #new width
        if 'new_width' in param.keys():
            self.new_width = param['new_width']
        else:
            self.new_width = 0
        #mirror
        if 'mirror' in param.keys():
            self.mirror = param['mirror']
        else:
            self.mirror = False

    def setup(self,bottom,top):
        self.get_param()

        self.txtlines = open(os.path.join(self.source, self.split + '.txt'),'r').read().splitlines()

        self.linen = len(self.txtlines)

        if self.shuffle:
            random.shuffle(self.txtlines)
        self.idx = 0
        self.img_shape = self.img_shape()

    def reshape(self,bottom,top):
        self.load()
        self.transform()
        top[0].reshape(*self.data.shape)
        top[1].reshape(*self.label.shape)

    def forward(self,bottom,top):
        top[0].data[...] = self.data
        top[1].data[...] = self.label

    def backward(self,top,propagate_down,bottom):
        pass

    def img_shape(self):
        im = Image.open(os.path.join(self.root_folder, self.txtlines[0].split(' ')[0]))
        im = np.array(im,dtype=np.float32)
        if len(im.shape) == 2:
            c = 1
        else:
            c = im.shape[2]
        if (self.new_height>0) and (self.new_width>0):
            return [self.new_height,self.new_width,c]
        else:
            return [im.shape[0],im.shape[1],c]

    def load_image(self, idx):
        im = Image.open(os.path.join(self.root_folder, self.txtlines[idx].split(' ')[0]))
        in_ = np.array(im, dtype=np.float32)
        if len(in_.shape) == 2:
            in_ = in_[np.newaxis,...]
        else:
            in_ = in_[:,:,::-1]
            in_ = in_.transpose((2,0,1))
        return in_


    def load_label(self, idx):
        im = Image.open(os.path.join(self.root_folder, self.txtlines[idx].split(' ')[1]))
        label = np.array(im, dtype=np.uint8)
        if len(label.shape) == 2:
            label = label[np.newaxis,...]
        else:
            label = label.transpose((2,0,1))
        return label

    def load(self):
        self.data_buf=[]
        self.label_buf=[]

        for i in range(self.batch_size):
            self.data_buf.append(self.load_image(self.idx))
            self.label_buf.append(self.load_label(self.idx))

            self.idx = self.idx + 1
            if self.idx == self.linen:
                self.idx = 0
                if self.shuffle:
                    random.shuffle(self.txtlines)

    def transform(self):
        self.data = np.zeros((self.batch_size, self.img_shape[2], self.img_shape[0], 
                              self.img_shape[1]), dtype=np.float32)
        self.label = np.zeros((self.batch_size, 1, self.img_shape[0], 
                               self.img_shape[1]), dtype=np.uint8)
        #resize
        if (self.new_height > 0) or (self.new_width > 0):
            rs_height = self.data.shape[2]
            rs_width  = self.data.shape[3]

            if self.new_height > 0:
                rs_height = self.new_height
            if self.new_width > 0:
                rs_width  = self.new_width
            
            for i in range(self.batch_size):
                new_data = cv2.resize(self.data_buf[i].transpose((1,2,0)),(rs_width,rs_height),
                                      interpolation = cv2.INTER_NEAREST)
                if len(new_data.shape) == 2:
                    new_data = new_data[np.newaxis,...]
                else:
                    new_data = new_data.transpose((2,0,1))
                self.data_buf[i] = new_data
                
                new_label = cv2.resize(self.label_buf[i].transpose((1,2,0)),(rs_width,rs_height),
                                       interpolation = cv2.INTER_NEAREST)
                if len(new_label.shape) == 2:
                    new_label = new_label[np.newaxis,...]
                else:
                    new_label = new_label.transpose((2,0,1))
                self.label_buf[i] = new_label

        for i in range(self.batch_size):
            self.data[i,:,:,:] = self.data_buf[i]
            self.label[i,:,:,:] = self.label_buf[i]
        #sub mean
        if len(self.mean_value)>0:
            if len(self.mean_value) != self.data.shape[1]:
                sys.exit(1)
            for i in range(self.data.shape[1]):
                self.data[:,i,:,:] = self.data[:,i,:,:] - self.mean_value[i]
        #mul scale
        if len(self.scale)>0:
            if len(self.scale) != self.data.shape[1]:
                sys.exit(2)
            for i in range(self.data.shape[1]):
                self.data[:,i,:,:] = self.data[:,i,:,:] * self.scale[i]
        #mirror
        if self.mirror and random.random() > 0.5:
            self.data = self.data[:,:,:,::-1]
            self.label = self.label[:,:,:,::-1]
