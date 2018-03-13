#!/bin/bash

##############################################################################
#######################   CONFIGURING DIR STRUCTURE   ########################
##############################################################################

ROOT_DIR=$(pwd)

DEPS_DIR=$ROOT_DIR/deps
mkdir $DEPS_DIR

SRC_DIR=$ROOT_DIR/deps/src
BIN_DIR=$DEPS_DIR/bin
INCLUDE_DIR=$DEPS_DIR/include
LIB_DIR=$DEPS_DIR/lib
LIB64_DIR=$DEPS_DIR/lib64

source export-flags.sh

##############################################################################
########################   DOWNLOAD AND UNZIP STEP   #########################
##############################################################################

./download-and-unzip-deps.sh

EXITSTATUS=$?
if [ $EXITSTATUS != 0 ]
then
    echo "Terminated."
    exit 1
fi

##############################################################################
############################   BUILD DEPS STEP   #############################
##############################################################################

echo "################   Build CMake   ################"
./build-scripts/build-cmake.sh
EXITSTATUS=$?
if [ $EXITSTATUS != 0 ]
then
    echo "CMake build failed."
    exit 1
fi

echo "################   Build ATLAS   ################"
./build-scripts/build-atlas.sh
EXITSTATUS=$?
if [ $EXITSTATUS != 0 ]
then
    echo "Atlas build failed."
    exit 1
fi
export LIBS="$LIBS -latlas -lcblas"

echo "################   Build hdf5   ################"
./build-scripts/build-hdf5.sh
EXITSTATUS=$?
if [ $EXITSTATUS != 0 ]
then
    echo "hdf5 build failed."
    exit 1
fi
export LIBS="$LIBS -lhdf5 -lhdf5_hl"

echo "################   Build lmdb   ################"
./build-scripts/build-lmdb.sh
EXITSTATUS=$?
if [ $EXITSTATUS != 0 ]
then
    echo "lmdb build failed."
    exit 1
fi
export LIBS="$LIBS -llmdb"

echo "################   Build snappy   ################"
./build-scripts/build-snappy.sh
EXITSTATUS=$?
if [ $EXITSTATUS != 0 ]
then
    echo "Snappy build failed."
    exit 1
fi
export LIBS="$LIBS -lsnappy"

echo "################   Build levedb   ################"
./build-scripts/build-leveldb.sh
EXITSTATUS=$?
if [ $EXITSTATUS != 0 ]
then
    echo "leveldb build failed."
    exit 1
fi
export LIBS="$LIBS -lleveldb"

echo "################   Build boost   ################"
./build-scripts/build-boost.sh
EXITSTATUS=$?
if [ $EXITSTATUS != 0 ]
then
    echo "Boost build failed."
    exit 1
fi
export LIBS="$LIBS -lboost_system -lboost_filesystem"

echo "################   Build OpenCV   ################"
./build-scripts/build-opencv.sh
EXITSTATUS=$?
if [ $EXITSTATUS != 0 ]
then
    echo "OpenCV build failed."
    exit 1
fi
export LIBS="$LIBS -lopencv_core -lopencv_highgui -lopencv_imgproc"

echo "################   Build gflags   ################"
./build-scripts/build-gflags.sh
EXITSTATUS=$?
if [ $EXITSTATUS != 0 ]
then
    echo "gflags build failed."
    exit 1
fi
export LIBS="$LIBS -lgflags"

echo "################   Build glog   ################"
./build-scripts/build-glog.sh
EXITSTATUS=$?
if [ $EXITSTATUS != 0 ]
then
    echo "glog build failed."
    exit 1
fi
export LIBS="$LIBS -lglog"

echo "################   Build protobuf   ################"
./build-scripts/build-protobuf.sh
EXITSTATUS=$?
if [ $EXITSTATUS != 0 ]
then
    echo "protobuf build failed."
    exit 1
fi
export LIBS="$LIBS -lprotobuf"

##############################################################################
###########################   BUILD CAFFE STEP   #############################
##############################################################################

echo "################   Build Caffe   ################"
./build-scripts/build-caffe.sh
EXITSTATUS=$?
if [ $EXITSTATUS != 0 ]
then
    echo "Caffe build failed."
    exit 1
fi
