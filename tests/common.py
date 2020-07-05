import os
import sys
import logging


logging.basicConfig(level=logging.DEBUG)


TESTS_DIR = os.path.dirname(__file__)
BR_HISICAM_ROOT = os.path.abspath(os.path.join(TESTS_DIR, ".."))


sys.path.insert(0, BR_HISICAM_ROOT)  # needed to import testcore package
