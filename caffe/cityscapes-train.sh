#!/bin/bash

mkdir /tmp/cityscapes
cp cityscapes/train.h5 /tmp/cityscapes/
build/tools/caffe train --solver=cityscapes/solver.prototxt $@
rm -rf /tmp/cityscapes

