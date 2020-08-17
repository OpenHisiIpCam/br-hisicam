#!/bin/bash

ROOT_DIR=$(realpath $(dirname $(readlink -f $0))/..)
BR_EXT_HISICAM_DIR=${ROOT_DIR}/br-ext-hisicam

BR_DIR=$ROOT_DIR/buildroot-2020.02
TOOLCHAINS_DIR=$ROOT_DIR/toolchains

FAMILY=
USE_STORAGE=N


while [[ $# > 0 ]]; do
    case $1 in
        "--use-storage") USE_STORAGE="Y"; shift;;
        "--family") FAMILY=$2; shift 2;;
        "--br") BR_DIR=$2; shift 2;;
        "--td") TOOLCHAINS_DIR=$2; shift 2;;
        *) echo "Invalid argument $1"; exit 1;;
    esac
done

# -------------------------------------------------------------------------------------------------
DEFCONFIG=$BR_EXT_HISICAM_DIR/configs/toolchains/${FAMILY}_defconfig
OUT_DIR=$TOOLCHAINS_DIR/$FAMILY
BUILD_DIR=$TOOLCHAINS_DIR/builds/$FAMILY

ENV_HASH=$( { sed -r '/^\s*$/d; s/ *$//; s/^ *//;' $DEFCONFIG | sort -; uname -mor; } | md5sum - | awk '{print $1}' )

STORAGE_PY=$ROOT_DIR/utils/storage.py
STORAGE_KEY=sdk-$FAMILY-$ENV_HASH.tar.gz
STORAGE_BUCKET=hisicam-buildroot-sdks
DOWNLOADED_TAR=$TOOLCHAINS_DIR/dl/$STORAGE_KEY

MAKE="make -C $BR_DIR BR2_EXTERNAL=$BR_EXT_HISICAM_DIR O=$BUILD_DIR"


# -------------------------------------------------------------------------------------------------
function log() {
    echo "--" $@ >&2
}


# -------------------------------------------------------------------------------------------------
function download_toolchain() {
    mkdir -p $(dirname $DOWNLOADED_TAR)

    $STORAGE_PY download --bucket $STORAGE_BUCKET --object-key $STORAGE_KEY --file $DOWNLOADED_TAR
    if [[ $? != 0 ]]; then
        log "Toolchain has not been downloaded"
        return 1
    fi
    log "Toolchain has been downloaded"

    mkdir -p $OUT_DIR
    tar -C $OUT_DIR --strip-components=1 -xf $DOWNLOADED_TAR && $OUT_DIR/relocate-sdk.sh
    if [[ $? != 0 ]]; then
        log "Toolchain has not been prepared"
        return 1
    fi
    log "Toolchain been prepared successfully"
}


# -------------------------------------------------------------------------------------------------
function upload_toolchain() {
    if ! $MAKE sdk; then
        log "Failed to build SDK"
        return 1
    fi

    eval $($MAKE -s --no-print-directory VARS=GNU_TARGET_NAME printvars)
    TAR=$BUILD_DIR/images/${GNU_TARGET_NAME}_sdk-buildroot.tar.gz
    if ! [[ -e $TAR ]]; then
        log "Could not find toolchain tar: $TAR"
        return 1
    fi

    ${STORAGE_PY} upload --bucket $STORAGE_BUCKET --object-key $STORAGE_KEY --file $TAR
    if [[ $? != 0 ]]; then
        log "Toolchain has not been uploaded"
        return 1
    fi
    log "Toolchain has been uploaded successfully"
}


# -------------------------------------------------------------------------------------------------
function make_toolchain() {
    log "Remove existing toolchain directory..."
    rm -rf $OUT_DIR

    if [[ $USE_STORAGE == "Y" ]] && download_toolchain; then
        return
    fi
    
    log "Build toolchain for $FAMILY locally"
    rm -rf $BUILD_DIR
    if ! { $MAKE BR2_DEFCONFIG=$DEFCONFIG defconfig && $MAKE prepare-sdk; } then
        log "Failed to build toolchain locally"
        return 1
    fi
    ln -sr $BUILD_DIR/host $OUT_DIR

    if [[ $USE_STORAGE == "Y" ]]; then
        upload_toolchain
    fi
}


make_toolchain
