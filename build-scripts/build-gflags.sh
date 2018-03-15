#!/bin/bash

ROOT_DIR=$(pwd)
DEPS_DIR=$ROOT_DIR/deps
SRC_DIR=$ROOT_DIR/deps/src
BIN_DIR=$DEPS_DIR/bin

cd $SRC_DIR/*gflags*
mkdir build
cd build
$BIN_DIR/cmake -DCMAKE_INSTALL_PREFIX=$DEPS_DIR -DCMAKE_CXX_FLAGS:STRING=-fPIC ..
make -s -j 4
make -s -j 4 install || exit -1
cd $ROOT_DIR 