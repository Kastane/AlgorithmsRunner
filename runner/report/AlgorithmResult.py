import re
import log
from pathlib import Path
from collections import namedtuple
from datetime import datetime

from datetime import timezone

from platforms.auxiliary.Misc import Misc

LOCAL_TIMEZONE = datetime.now(timezone.utc).astimezone().tzinfo


class AlgorithmResult(object):
    __result_patt = r'.*: ([\w-]+) (-?\d+(\.\d+)?)'

    def __init__(self, component, cfg, algorithm_name, algorithm_out=None, algorithm_err=None,
                 compile_time=None, bin_size=None):

        self.__cfg = cfg
        self.__component = component
        self.__name = algorithm_name
        self.__out = algorithm_out
        self.__err = algorithm_err
        self.__result_val = self.__parse_result()
        self.__ext_time = None
        self.__mem_val = None
        local_rss_path = Path(Misc.local_rss_path)

        if local_rss_path.is_file():
            rss_out = local_rss_path.read_text()
            log.debug("rss.out: '{}'", rss_out)
            self.__mem_val = self.__parse_rss(rss_out)
            self.__ext_time = self.__parse_ext_time(rss_out)
            local_rss_path.unlink()

        self.__time = compile_time
        self.__bin_size = bin_size

    @property
    def result_val(self):
        return self.__result_val

    @property
    def name(self):
        return self.__name

    @property
    def rss(self):
        return self.__mem_val

    @property
    def time(self):
        return self.__time

    @property
    def ext_time(self):
        return self.__ext_time

    @property
    def bin_size(self):
        return self.__bin_size

    @property
    def component(self):
        return self.__component

    def __parse_result(self):
        log.debug("Result: '{}'".format(self.__out))

        if not self.__out:
            return None
        mtch = re.search(self.__result_patt, self.__out)

        if mtch and mtch.groups()[0] == Path(self.__name).stem:
            return float(mtch.groups()[1])

        return None

    def __parse_rss(self, rss_out):
        rss_r = r"(?:Maximum resident set size|Max RSS)[^:]*:\s*(\d*)"
        m = re.search(rss_r, rss_out)

        if m is None:
            return None

        return int(m.groups()[0])

    def __parse_ext_time(self, rss_out):
        tm_r = r"(?:Elapsed.*\(h:mm:ss or m:ss\)|Real time)[^:]*:\s*(?:(\d*):)?(\d*)(?:.(\d*))?"
        t = re.search(tm_r, rss_out)

        if t is None:
            return None

        tmp = t.groups()

        if tmp[0] is None:
            return round(float(str(tmp[1]) + "." + tmp[2]), 5)

        return round(int(tmp[0]) * 60 + float(str(tmp[1]) + "." + tmp[2]), 5)
