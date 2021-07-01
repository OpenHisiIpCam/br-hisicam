import os
import sys
import logging
import shutil
from .utils import parse_kv_lines
from .make import Make
from .vars import BR_HISICAM_ROOT, BASE_WORKDIR


class BrHisiCam:
    def __init__(self, board, output_dir=None, toolchains_dir=None, clean=False, stdout=None, stderr=None):
        if output_dir is None:
            output_dir = os.path.join(BASE_WORKDIR, board)
        if toolchains_dir is None:
            toolchains_dir = os.path.join(BASE_WORKDIR, "toolchains")

        output_dir = os.path.abspath(output_dir)
        toolchains_dir = os.path.abspath(toolchains_dir)

        for p in (output_dir, toolchains_dir):
            if clean and os.path.exists(p):
                logging.info(f"Remove existing BR directory '{p}'")
                shutil.rmtree(p)
            os.makedirs(p, exist_ok=True)

        if stdout is None:
            stdout = sys.stderr.fileno()  # all output is redirected to stderr by default

        self._make = Make(BR_HISICAM_ROOT,
            args=[f"BOARD={board}", f"OUT_DIR={output_dir}", f"TOOLCHAINS_DIR={toolchains_dir}", "USE_TOOLCHAIN_STORAGE=y"],
            stdout=stdout, stderr=stderr
        )

        self._board = board
        self._output_dir = output_dir
        self._toolchains_dir = toolchains_dir

    def make_all(self, *args):
        self._make.check_call(["all", *args])

    def make_board_info(self):
        return parse_kv_lines(self._make.get_output_lines(["board-info"]))

    def make_overlayed_rootfs(self, overlays, fs_type="squashfs"):
        overlays_csv = ",".join(os.path.abspath(i) for i in overlays)
        self._make.check_call([f"ROOTFS_OVERLAYS={overlays_csv}", f"overlayed-rootfs-{fs_type}"])

    @property
    def output_dir(self):
        return self._output_dir

    @property
    def board(self):
        return self._board