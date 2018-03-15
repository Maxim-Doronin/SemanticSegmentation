#!/bin/bash

ROOT_DIR=$(pwd)
DEPS_DIR=$ROOT_DIR/deps
SRC_DIR=$ROOT_DIR/deps/src

BOOST_DIR=$SRC_DIR/boost*
cd $BOOST_DIR
BOOST_DIR=$(pwd)
./bootstrap.sh --prefix=$DEPS_DIR --with-libraries=all
./b2 -j 8
./b2 -j 8 install || exit -1
cd $ROOT_DIR