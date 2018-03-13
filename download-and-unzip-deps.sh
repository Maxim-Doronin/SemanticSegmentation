#!/bin/bash

ROOT_DIR=$(pwd)
ZIPS_DIR=$ROOT_DIR/deps/zips
mkdir $ZIPS_DIR
SRC_DIR=$ROOT_DIR/deps/src
mkdir $SRC_DIR

_url_cmake="https://cmake.org/files/v3.10/cmake-3.10.2.tar.gz"
_url_boost="http://sourceforge.net/projects/boost/files/boost/1.65.1/boost_1_65_1.zip"
_url_atlas="https://sourceforge.net/projects/math-atlas/files/Stable/3.10.2/atlas3.10.2.tar.bz2"
_url_hdf5="https://support.hdfgroup.org/ftp/HDF5/current/src/hdf5-1.10.1.tar"
_url_leveldb="https://github.com/google/leveldb/archive/v1.20.tar.gz"
_url_lmdb="https://github.com/LMDB/lmdb/archive/mdb.master.zip"
_url_gflags="https://github.com/gflags/gflags/archive/v2.2.1.tar.gz"
_url_glog="https://github.com/google/glog/archive/v0.3.5.tar.gz"
_url_protobuf="https://github.com/google/protobuf/releases/download/v3.5.1/protobuf-all-3.5.1.tar.gz"

wget $_url_cmake -P $ZIPS_DIR
wget $_url_boost -P $ZIPS_DIR
wget $_url_atlas -P $ZIPS_DIR
wget $_url_hdf5 -P $ZIPS_DIR
wget $_url_leveldb -P $ZIPS_DIR
wget $_url_lmdb -P $ZIPS_DIR
wget $_url_gflags -P $ZIPS_DIR
wget $_url_glog -P $ZIPS_DIR
wget $_url_protobuf -P $ZIPS_DIR

if [ $(ls $ZIPS_DIR | wc -l) != 9 ]
then
    echo "Can't get all sources. Try to run ./download-and-unzip-deps.sh again"
    exit 1
fi

for file in $(ls $ZIPS_DIR/*tar*)
do
    echo "Unzip $file"
    tar -xf $file -C $SRC_DIR
done

for file in $(ls $ZIPS_DIR/*zip*)
do
    echo "Unzip $file"
    unzip -q $file -d $SRC_DIR
done