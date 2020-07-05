import subprocess
import logging
import sys


class Make:
    def __init__(self, root_dir, args=[], stdout=None, stderr=None):
        self._root_dir = root_dir
        self._args = ["make", "-s", "--no-print-directory"] + args
        self._proc_stdout = stdout
        self._proc_stderr = stderr

    def check_call(self, args):
        args = self._args + args
        logging.debug(f"Execute {args} in {self._root_dir} ...")
        subprocess.check_call(args,
            cwd=self._root_dir,
            stdout=self._proc_stdout,
            stderr=self._proc_stderr
        )

    def check_output(self, args):
        args = self._args + args
        logging.debug(f"Execute {args} in {self._root_dir} ...")
        output = subprocess.check_output(args,
            cwd=self._root_dir,
            stderr=self._proc_stderr
        )
        logging.debug(f"Output of {args} command: {output}")
        return output

    def get_output_lines(self, args):
        out = self.check_output(args)
        return [l.strip() for l in out.decode("utf-8").split("\n")]
