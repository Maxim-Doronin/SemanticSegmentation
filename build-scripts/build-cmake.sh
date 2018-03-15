#!/bin/bash

ROOT_DIR=$(pwd)
DEPS_DIR=$ROOT_DIR/deps
SRC_DIR=$ROOT_DIR/deps/src

cd $SRC_DIR/cmake*
./bootstrap --prefix=$DEPS_DIR
make -s -j 8
make -s -j 8 install || exit -1
cd $ROOT_DIR