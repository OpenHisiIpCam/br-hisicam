import os
import json
import logging
from .env import BrHisiCam, HiburnClient


# -------------------------------------------------------------------------------------------------
def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


# -------------------------------------------------------------------------------------------------
logging.basicConfig(level=logging.DEBUG)

TESTENV_DIR = os.path.dirname(__file__)
BR_HISICAM_ROOT = os.path.abspath(os.path.join(TESTENV_DIR, "../.."))
HIBURN_APP = os.path.abspath(os.path.join(TESTENV_DIR, "../../hiburn/hiburn_app.py"))

#POWER_APP = "/home/wsnk/Development/hi3519v101_go/burner/power2.py"  # TODO - do it properly
POWER_APP = os.path.abspath(os.path.join(TESTENV_DIR, "power2.py"))

# JSON contains parameters for all testable devices
DEVICE_LIST_PATH = os.path.join(TESTENV_DIR, "boards.json")

# Hosts's IPv4 address and netmask length used for tests
HOST_IP_MASK = "192.168.10.2/24"


# -------------------------------------------------------------------------------------------------
DEVICE_LIST = load_json(DEVICE_LIST_PATH)
br_hisicam = BrHisiCam(BR_HISICAM_ROOT)
hiburn = HiburnClient(app_path=HIBURN_APP, device_list=DEVICE_LIST, power_app_path=POWER_APP, host_ip_mask=HOST_IP_MASK)
