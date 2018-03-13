#!/bin/bash

cd ..
ROOT_DIR=$(pwd)
DEPS_DIR=$ROOT_DIR/deps
SRC_DIR=$ROOT_DIR/deps/src

HDF5_DIR=$SRC_DIR/*hdf5*
cd $HDF5_DIR
HDF5_DIR=$(pwd)
./configure --prefix=$DEPS_DIR --shared
make -s prefix=$DEPS_DIR
make -s install prefix=$DEPS_DIR || exit -1
cd $ROOT_DIR