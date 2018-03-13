#!/bin/bash

cd ..
ROOT_DIR=$(pwd)
DEPS_DIR=$ROOT_DIR/deps
SRC_DIR=$ROOT_DIR/deps/src

LMDB_DIR=$SRC_DIR/*lmdb*
cd $LMDB_DIR
LMDB_DIR=$(pwd)
cd $LMDB_DIR/libraries/liblmdb
make -s prefix=$DEPS_DIR
make -s install prefix=$DEPS_DIR || exit -1
cd $ROOT_DIR