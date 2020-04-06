import os
import pytest
import subprocess
import logging
import socket
import time
from testenv import DEVICE_LIST, br_hisicam, hiburn



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

def cam_test(board):
    logging.info(f"Build uImage and rootfs for {board}...")
    br_hisicam.make_board(board)

    uimage_path = br_hisicam.uimage_path(board)
    assert os.path.exists(uimage_path)

    rootfs_image_path = br_hisicam.rootfs_image_path(board)
    assert os.path.exists(rootfs_image_path)

    logging.info(f"Upload images on {board} test device and boot it...")
    info = br_hisicam.info(board)
    hiburn.boot(board, uimage=uimage_path, rootfs=rootfs_image_path, device_info=info)

    logging.info(f"Test echo_server runing on device...")
    conn = connect(DEVICE_LIST[board]["ip_addr"], 20040)
    msg = f"Hello {board}!"
    conn.send(msg.encode("ascii"))
    resp = conn.recv(1024).decode("ascii", errors="ignore")
    assert resp == f"YOU SAID: {msg}"

def test_cam1():   #OK
   board = "jvt_s274h19v-l29_hi3519v101_imx274"
   cam_test(board)

def test_cam2():    #OK
    board = "xm_ivg-85hf20pya-s_hi3516ev200_imx307"
    cam_test(board)

def test_cam3():   #OK
    board = "xm_53h20-s_hi3516cv100_imx122"
    cam_test(board)

def test_cam4():   #OK
    board = "xm_ivg-hp203y-se_hi3516cv300_imx291"
    cam_test(board)

def test_cam5():    #OK
    board = "xm_ivg-hp201y-se_hi3516cv300_imx323"
    cam_test(board)

def test_cam6():   #OK
    board = "jvt_s323h16xf_hi3516cv300_imx323"
    cam_test(board)

def test_cam7():   #OK
    board = "ruision_rs-h622qm-b0_hi3516cv300_imx323"
    cam_test(board)

def test_cam8():    #uboot locked no output
    board = "xm_ivg-85hg50pya-s_hi3516ev300_imx335"
    cam_test(board)

def test_cam9():   #OK
    board = "xm_ipg-83h50p-b_hi3516av100_imx178"
    cam_test(board)

def test_cam10():   #OK
    board = "xm_ipg-83he20py-s_hi3516ev100_imx323"
    cam_test(board)

def test_cam11():  #OK
    board = "xm_ivg-83h80nv-be_hi3516av200_os08a10"
    cam_test(board)

def test_cam13():   #OK
    board = "ssqvision_on335h16d_hi3516dv300_imx335"
    cam_test(board)

def test_cam14():  #OK
    board = "jvt_s226h19v-l29_hi3519v101_imx226"
    cam_test(board)

def test_cam15():  #OK
    board = "xm_53h20-ae_hi3516cv100_imx222"
    cam_test(board)

def test_cam16():   #OK
    board = "xm_83h40pl-b_hi3516av100_ov4689"
    cam_test(board)

#def test_cam17():   #uboot network is not working
#    board = "ssqvision_unknown_hi3519v101_imx326"
#    cam_test(board)

def test_cam18():   #OK
    board = "ssqvision_on290h16d_hi3516dv100_imx290"
    cam_test(board)

