#!/bin/bash

#rm -rf /tmp/cityscapes
#mkdir /tmp/cityscapes
#cp cityscapes/train.h5 /tmp/cityscapes/
#cp cityscapes/val.h5 /tmp/cityscapes/
#ls /tmp/cityscapes
echo kek
cd cityscapes
python solve_test.py
#../build/tools/caffe train -gpu 0 --solver=solver.prototxt
#rm -rf /tmp/cityscapes

