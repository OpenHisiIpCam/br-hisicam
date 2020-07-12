import os
import logging
import subprocess


class Hiburn:
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

    def execute(self, args, stdout=None, stderr=None, timeout=None):
        args = [str(arg) for arg in args]
        logging.debug("Execute: {}".format(" ".join(args)))
        subprocess.check_call(
            [self.app_path, *args],
            stdout=stdout,
            stderr=stdout,
            timeout=timeout
        )

    def boot(self, device_id, uimage, rootfs, device_info, **kwargs):
        self.execute(args=[
            *self.get_device_args(device_id),
            "--mem-start_addr", device_info["MEM_START_ADDR"],
            "--mem-linux_size", device_info["RAM_LINUX_SIZE"],
            "boot",
            "--uimage", uimage,
            "--rootfs", rootfs
        ], **kwargs)
