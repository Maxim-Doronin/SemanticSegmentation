#!/bin/bash

ROOT_DIR=$(pwd)
DEPS_DIR=$ROOT_DIR/deps
SRC_DIR=$ROOT_DIR/deps/src

ATLAS_DIR=$SRC_DIR/ATLAS*
cd $ATLAS_DIR
ATLAS_DIR=$(pwd)
mkdir build
cd build
$ATLAS_DIR/configure --prefix=$DEPS_DIR --shared -Fa alg -fPIC
make -s
make -s install || exit -1
cd $ROOT_DIR