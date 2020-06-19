import os
import json
from .vars import *
from .brhisicam import BrHisiCam
from .make import Make
from .hiburn import Hiburn


def list_boards():
    return Make(BR_HISICAM_ROOT).get_output_lines(["list-configs"])


hiburn = Hiburn(
    app_path=HIBURN_APP,
    device_list=DEVICE_LIST,
    power_app_path=POWER_APP,
    host_ip_mask=HOST_IP_MASK
)