#!/bin/bash

cd ..
ROOT_DIR=$(pwd)
DEPS_DIR=$ROOT_DIR/deps
SRC_DIR=$ROOT_DIR/deps/src

cd $SRC_DIR/*glog*
./configure --prefix=$DEPS_DIR
make -s
make -s install || exit -1
cd $ROOT_DIR