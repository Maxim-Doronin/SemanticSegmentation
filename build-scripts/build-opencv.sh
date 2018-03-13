#!/bin/bash

cd ..
ROOT_DIR=$(pwd)
DEPS_DIR=$ROOT_DIR/deps
SRC_DIR=$ROOT_DIR/deps/src
BIN_DIR=$ROOT_DIR/deps/bin

cd $SRC_DIR
git clone https://github.com/opencv/opencv.git
cd $SRC_DIR/opencv
mkdir build
cd build
$BIN_DIR/cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=$DEPS_DIR ..
make -s
make -s install || exit -1
cd $ROOT_DIR