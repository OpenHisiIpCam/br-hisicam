#!/usr/bin/env python3
import os
import sys
import socket
import time
import logging
from contextlib import contextmanager
import testcore


@contextmanager
def stage():
    try:
        yield None
        print("OK", end=" | ", flush=True)
    except:
        print("FAILED", end=" | ", flush=True)
        raise


def connect(host, port, timeout=60):
    end_time = time.monotonic() + timeout
    while True:
        try:
            logging.info(f"Connect to {host}:{port}...")
            conn = socket.create_connection(address=(host, port))
            logging.info(f"Connected to {host}:{port}")
            return conn
        except:
            if time.monotonic() > end_time:
                raise


def check_board(board):
    print(board, end=" | ", flush=True)
    br_hisicam = testcore.BrHisiCam(board=board)

    with stage():
        logging.info(f"Build BR...")
        br_hisicam.make_all()

    with stage():
        logging.info(f"Build echo server...")
        example_app_path = os.path.join(testcore.BR_HISICAM_ROOT, "examples/echo_server")
        testcore.Make(
            example_app_path,
            stdout=sys.stderr.fileno()
        ).check_call([f"OUT_DIR={br_hisicam.output_dir}", "build"])
        br_hisicam.make_overlayed_rootfs(overlays=[os.path.join(example_app_path, "overlay")])

    with stage():
        logging.info(f"Deploy...")
        uimage_path = os.path.join(br_hisicam.output_dir, "images/uImage")
        rootfs_image_path = os.path.join(br_hisicam.output_dir, "images/rootfs-overlayed.squashfs")
        info = br_hisicam.make_board_info()
        testcore.hiburn.boot(board,
            uimage=uimage_path,
            rootfs=rootfs_image_path,
            device_info=info,
            stdout=sys.stderr.fileno(),
            timeout=180
        )

    with stage():
        logging.info(f"Test echo_server runing on device...")
        conn = connect(testcore.DEVICE_LIST[board]["ip_addr"], 20040)
        msg = f"Hello {board}!"
        conn.send(msg.encode("ascii"))
        resp = conn.recv(1024).decode("ascii", errors="ignore")
        assert resp == f"YOU SAID: {msg}"


# -------------------------------------------------------------------------------------------------
logging.basicConfig(level=logging.DEBUG)


print(
    " Board | Build BR | Build echo server | Deploy | Test | Total \n"
    "-------|----------|-------------------|--------|------|-------",
    flush=True
)

for board in testcore.DEVICE_LIST.keys():
    try:
        check_board(board)
        print(":thumbsup:", flush=True)
    except:
        logging.exception(f"Check of board {board} failed")
        print("", flush=True)
