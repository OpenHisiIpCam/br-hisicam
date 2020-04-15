import os.path
import subprocess
import logging
from telnetlib import Telnet


TESTENV_DIR = os.path.dirname(__file__)


# -------------------------------------------------------------------------------------------------
class HiburnClient:
    def __init__(self, app_path, device_list, power_app_path, host_ip_mask=None):
        self.app_path = app_path  # hiburn executable path
        self.device_list = device_list
        self.power_app_path = power_app_path

        self.host_ip_mask = host_ip_mask

    def reset_power_cmd(self, num):
        return f"{self.power_app_path} --num {num} reset"

    def get_device_args(self, device_id):
        device_desc = self.device_list[device_id]
        return [
            "--reset-cmd", self.reset_power_cmd(device_desc["power_num"]),
            "--serial", device_desc["serial"],
            "--net-device_ip", device_desc["ip_addr"],
            "--net-host_ip_mask", self.host_ip_mask,
        ]

    def execute(self, args):
        args = [str(arg) for arg in args]
        logging.debug("Execute: {}".format(" ".join(args)))
        subprocess.check_call([self.app_path, *args])

    def boot(self, device_id, uimage, rootfs, device_info):
        self.execute([
            *self.get_device_args(device_id),
            "--mem-start_addr", device_info["MEM_START_ADDR"],
            "--mem-linux_size", device_info["RAM_LINUX_SIZE"],
            "boot",
            "--uimage", uimage,
            "--rootfs", rootfs
        ])


# -------------------------------------------------------------------------------------------------
class BrHisiCam:
    def __init__(self, root_dir):
        self.root = root_dir
        self.configs = self._get_config_list()

    def _get_make_output_lines(self, args):
        out = subprocess.check_output(["make", *args], cwd=self.root)
        return [l.strip() for l in out.decode("utf-8").split("\n")]

    def _get_config_list(self):
        return self._get_make_output_lines(["list-configs"])

    def make_board(self, board_id, rootfs_overlays=None):
        params = [
            f"BR2_ROOTFS_POST_BUILD_SCRIPT={TESTENV_DIR}/rootfs_post_build.sh"
        ]
        if rootfs_overlays is not None:
            params.append(f"BR2_ROOTFS_OVERLAY=\"{' '.join(rootfs_overlays)}\"")
        subprocess.check_call(["make", *params, f"{board_id}_defconfig"], cwd=self.root)

    def info(self, board_id):
        info = {}
        for l in self._get_make_output_lines([f"{board_id}_info"]):
            if l.find('=') != -1:
                key, value = l.split("=")
                info[key] = value
        return info

    def output_dir(self, board_id):
        return os.path.join(self.root, f"output/{board_id}")

    def uimage_path(self, board_id):
        return os.path.join(self.output_dir(board_id), "images/uImage")

    def rootfs_image_path(self, board_id):
        return os.path.join(self.output_dir(board_id), "images/rootfs.squashfs")
