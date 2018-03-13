#!/bin/bash

cd ..
ROOT_DIR=$(pwd)
DEPS_DIR=$ROOT_DIR/deps
SRC_DIR=$ROOT_DIR/deps/src

cd $SRC_DIR/*leveldb*
make -s prefix=$DEPS_DIR cc="-fPIC" || exit -1
find . -name "libleveldb.*" -exec cp {} $DEPS_DIR/lib \;
cp -r include/leveldb $DEPS_DIR/include/

cd $ROOT_DIR