#!/bin/bash
# Script to be used in BR2_ROOTFS_POST_BUILD_SCRIPT variable

TESTENV_DIR=`cd $(dirname $0) && pwd`

make -C $TESTENV_DIR/echo_server BR_HOST_DIR=$HOST_DIR build
if [ $? != 0 ]; then
    echo "Failed to build echo server" >&2
    exit -1
fi

cp $TESTENV_DIR/echo_server/echo_server $TARGET_DIR/bin/echo_server
cp $TESTENV_DIR/echo_server/run.sh $TARGET_DIR/etc/init.d/S99echo_server
