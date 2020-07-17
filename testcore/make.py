import subprocess
import logging
import sys
from contextlib import contextmanager


@contextmanager
def maybe_open1(out):
    if isinstance(out, str):
        with open(out, "ab") as f:
            yield f
    else:
        yield out


@contextmanager
def maybe_open2(stdout, stderr):
    with maybe_open1(stdout) as fout:
        if isinstance(stderr, str):
            if stderr == stdout:
                yield fout, fout
            else:
                with open(stderr, "ab") as ferr:
                    yield fout, ferr
        else:
            yield fout, stderr


class Make:
    def __init__(self, root_dir, args=[], stdout=None, stderr=None, verbose=False):
        self._root_dir = root_dir
        self._args = ["make"] + args
        if not verbose:
            self._args += ["-s", "--no-print-directory"]
        self._proc_stdout = stdout
        self._proc_stderr = stderr

    def check_call(self, args):
        args = self._args + args
        logging.debug(f"Execute {args} in {self._root_dir}, stdout={self._proc_stdout}, stderr={self._proc_stderr}")
        
        with maybe_open2(self._proc_stdout, self._proc_stderr) as (stdout, stderr):
            subprocess.check_call(args,
                cwd=self._root_dir,
                stdout=stdout,
                stderr=stderr
            )

    def check_output(self, args):
        args = self._args + args
        logging.debug(f"Execute {args} in {self._root_dir} ...")

        with maybe_open1(self._proc_stderr) as stderr:
            output = subprocess.check_output(args,
                cwd=self._root_dir,
                stderr=self.stderr
            )

        logging.debug(f"Output of {args} command: {output}")
        return output

    def get_output_lines(self, args):
        out = self.check_output(args)
        return [l.strip() for l in out.decode("utf-8").split("\n")]
