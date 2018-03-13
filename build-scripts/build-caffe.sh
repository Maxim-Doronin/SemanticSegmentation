#!/bin/bash

cd ..
ROOT_DIR=$(pwd)
DEPS_DIR=$ROOT_DIR/deps
SRC_DIR=$ROOT_DIR/deps/src

module load cuda/cuda-8.0

cd $ROOT_DIR/caffe
make -s -j 8 all
make -s -j 8 pycaffe
make -s -j 8 test
make -s runtest
cd $ROOT_DIR