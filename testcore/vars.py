import os
from . import utils


TESTCORE_DIR = os.path.dirname(__file__)
BR_HISICAM_ROOT = os.path.abspath(os.path.join(TESTCORE_DIR, ".."))

HIBURN_APP = os.path.abspath(os.path.join(BR_HISICAM_ROOT, "hiburn/hiburn_app.py"))
POWER_APP = os.path.abspath(os.path.join(TESTCORE_DIR, "power2.py"))

# directory that contains all build&test artifacts
BASE_WORKDIR = os.environ.get(
    "BRHISICAM_TEST_WORKDIR",
    os.path.abspath(os.path.join(os.getcwd(), "br_hisicam-workdir"))
)

# JSON contains parameters for all testable devices
DEVICE_LIST_PATH = os.path.join(TESTCORE_DIR, "boards.json")
DEVICE_LIST = utils.load_json(DEVICE_LIST_PATH)

# Hosts's IPv4 address and netmask length used for tests
HOST_IP_MASK = "192.168.10.2/24"
