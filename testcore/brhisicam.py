import os
import sys
import logging
import shutil
from .utils import parse_kv_lines
from .make import Make
from .vars import BR_HISICAM_ROOT, BASE_WORKDIR


class BrHisiCam:
    def __init__(self, board, output_dir=None, clean=False):
        if output_dir is None:
            output_dir = os.path.join(BASE_WORKDIR, board)

        output_dir = os.path.abspath(output_dir)
        if clean and os.path.exists(output_dir):
            logging.info(f"Remove existing BR output directory '{output_dir}'")
            shutil.rmtree(output_dir)

        os.makedirs(output_dir, exist_ok=True)

        self._make = Make(BR_HISICAM_ROOT,
            args=[f"BOARD={board}", f"OUT_DIR={output_dir}"],
            stdout=sys.stderr.fileno()  # all logs are redirected to stderr
        )

        self._board = board
        self._output_dir = output_dir

    def make_all(self):
        self._make.check_call(["all"])

    def make_board_info(self):
        return parse_kv_lines(self._make.get_output_lines(["board-info"]))

    def make_overlayed_rootfs(self, overlays, fs_type="squashfs"):
        overlays_csv = ",".join(os.path.abspath(i) for i in overlays)
        self._make.check_call([f"ROOTFS_OVERLAYS={overlays_csv}", f"overlayed-rootfs-{fs_type}"])

    @property
    def output_dir(self):
        return self._output_dir
