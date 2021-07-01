#!/bin/bash

TESTCORE_DIR=$(dirname $(readlink -f $0))
WORKDIR=$TESTCORE_DIR/../br_hisicam-workdir
BOARD=$1

OUT_DIR=$WORKDIR/$BOARD
TOOLCHAINS_DIR=$WORKDIR/toolchains
TESTCORE="python -m testcore --board $BOARD --output_dir $OUT_DIR --toolchains_dir $TOOLCHAINS_DIR"

cd $TESTCORE_DIR/..

$TESTCORE make_all
make -C ./examples/echo_server OUT_DIR=$OUT_DIR clean build rootfs-squashfs
$TESTCORE deploy --rootfs-image $OUT_DIR/images/rootfs-overlayed.squashfs

echo "Hello, board $BOARD!" | nc -vvv $($TESTCORE show_ip) 20040