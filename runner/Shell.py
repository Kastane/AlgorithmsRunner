import collections
import subprocess
import threading
import re
import os
import log
from Colors import Colors
from platforms.auxiliary.Misc import Misc


class ShellBase:
    class Result:
        def __init__(self, ret=None, out=None, err=None, tm=None):
            self.ret = ret
            self.out = out
            self.err = err
            self.tm = tm


    def _run_shell(self, cmd, measure_time):
        raise NotImplementedError()

    def run_with_config(self, cmd, measure_time):
        command_parts = []

        command_parts.append(cmd)

        dbg_cmd = " \\\n    ".join(command_parts)
        log.debug(f"> {dbg_cmd}")
        run_cmd = " ".join(command_parts)

        return self._run_shell(cmd, measure_time)

    def run(self, cmd, measure_time=False):
        return self.run_with_config(cmd, measure_time)

    def run_n_check_result(self, cmd, measure_time=True):
        res = self.run(cmd, measure_time)
        if res.ret != 0:
            print(Colors.Green + "STDOUT:" + Colors.End)
            print(Colors.Red + "STDERR:\n" + Colors.End)
            print(Colors.Red + res.err + Colors.End)
            print(Colors.Red + cmd + " returned " + str(res.ret) + Colors.End)
            return None
        else:
            return res

class ShellLinux(ShellBase):
    def __init__(self):
        super().__init__()

    def _run_shell(self, cmd, measure_time):
        if measure_time:
            cmd = "time -p " + cmd
    

        proc = subprocess.Popen(cmd, shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

        res = proc.communicate()
        result = self.Result()
        result.ret = proc.poll()
        result.out = res[0].decode("utf-8")
        result.err = res[1].decode("utf-8")

        log.debug(result.out)
        log.debug(Colors.Red + result.err + Colors.End)

        if measure_time:
            mtch = re.search(r"real\s*(\d*)\.(\d*)", result.err)
            result.tm = float(mtch.groups()[0]) + float("0." + mtch.groups()[1])
        else:
            result.tm = 0

        return result