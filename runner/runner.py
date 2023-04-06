#! /usr/bin/python3

import argparse
import re
import os
import copy
import json
import glob
import log
from datetime import datetime
from datetime import timezone
from Shell import ShellLinux
from Algorithm import Algorithm
from Colors import Colors
from platforms.auxiliary.Compilers import Compilers
from report.TextReport import TextReport
from utils import import_module


class AlgorithmRunner:
    __linux_sh = None

    # platforms
    __RUST_HOST = ("rusthost", "rh")
    __JAVA_HOST = ("javahost", "jh")

    __TARGETS = (__RUST_HOST, __JAVA_HOST)

    __HOST_TARGETS = __JAVA_HOST + __RUST_HOST

    __LANG = {__RUST_HOST[0]: "rust",
              __JAVA_HOST[0]: "java",
              }

    __EXT = {'java': ".java",
             'rust': ".rt"}

    __SCR_PATH = os.path.realpath(os.path.dirname(__file__))
    __ROOT_PATH = os.path.join(__SCR_PATH, "..")
    __FW_PATH = os.path.join(__ROOT_PATH, "framework")


    def __init__(self, target):
        self.__target = self.__normalize_target(target)
        log.debug("AlgorithmRunner init")
        self.__platform_module = None

        for platform in glob.glob(os.path.join(self.__SCR_PATH, "platforms", "*.py")):
            p_name = os.path.splitext(os.path.basename(platform))[0].lower()
            if p_name == self.__target:
                self.__platform_module = import_module("platform", platform)

    @property
    def target_lang(self):
        return self.__LANG[self.__target]

    def run_algorithm_wrapper(self, algorithm_path, args, result_series):
        target_workdir = '/'.join(algorithm_path.split('/')[:-3])
	
        cfg = {}
        cfg["warmupIters"] = args.warmup_iters
        cfg["measureIters"] = args.measure_iters
        cfg["measureTime"] = args.measure_time
        cfg["threadAmount"] = 1
        cfg["workDir"] = target_workdir
        cfg['target'] = args.target

        algorithm = Algorithm()
        algorithm.prm = Algorithm.Params(target=args.target,
                                         lang=self.target_lang,
                                         linux_sh=self.__linux_sh,
                                         algorithm_path=algorithm_path,
                                         framework_dir=self.__FW_PATH,
                                         config=cfg,
                                         timeout=args.timeout)

        measure_iters = args.measure_iters
        if not measure_iters:
            measure_iters = 1

        platform = self.__platform_module.Platform(algorithm.prm)

        try:
            res_arr = algorithm.run_algorithm(platform, measure_iters)
        except BaseException:
            platform.print_debug_info()
            raise

        result_series.append(res_arr)

    def parse_input(self, input_str, inputs):
        algorithm_realpath = input_str

        if os.path.isfile(algorithm_realpath):
            log.debug("input is file")
            self.__check_algorithm_lang(algorithm_realpath)
            inputs.add(algorithm_realpath)

        elif os.path.isdir(algorithm_realpath):
            log.debug(f"{Colors.Red}input is directory {algorithm_realpath}{Colors.End}")
            self.__parse_directory(algorithm_realpath, inputs)

        else:
            raise Exception("Not expected type of path: " + algorithm_realpath)

    def run_for_file(self, algorithm_path, args, result_series):
        try:
            self.run_algorithm_wrapper(algorithm_path, args, result_series)
        except (KeyboardInterrupt):
            raise
        except BaseException:
            log.exception()

    def __parse_directory(self, algorithm_real_dir, inputs):
        algorithm_list = os.listdir(algorithm_real_dir)
        log.debug(f"{Colors.Red}algorithmsets list {str(algorithmset_list)}{Colors.End}")

        for algorithmset in algorithmset_list:
            log.debug(f"{Colors.Red}algorithmset {algorithmset}{Colors.End}")
            algorithmset_realpath = os.path.join(algorithm_real_dir, algorithmset)

            if os.path.isdir(algorithmset_realpath):
                subdirs = list(set(os.listdir(algorithmset_realpath)))
                subdirs.sort()
                log.debug(f"{Colors.Red}algorithmset dirs {str(subdirs)}{Colors.End}")

                for algorithm_dir in subdirs:
                    log.debug(f"{Colors.Red}algorithm subdir {algorithm_dir}{Colors.End}")
                    algorithm_file = os.path.join(algorithmset_realpath, algorithm_dir, self.target_lang,
                                              algorithm_dir + self.__EXT[self.target_lang])

                    if os.path.exists(algorithm_file):
                        inputs.add(algorithm_file)

    def __normalize_target(self, target):
        for t in self.__TARGETS:
            if target in t:
                return t[0]

        return None

    def __check_algorithm_lang(self, algorithm_path):
        # Getting folder of algorithm, which name must be similar to language
        algorithm_lang = os.path.basename(os.path.dirname(algorithm_path))

        if algorithm_lang != self.target_lang:
            raise Exception(f"Algorithm language is not supported for given target,\
                              detected language is {algorithm_lang}")

    def __setup_shell(self):
        self.__linux_sh = ShellLinux()
        
    def main(self, cmd_args):
        cmd_args.target = self.__normalize_target(cmd_args.target)

        self.__setup_shell()

        result_series = []
        input_str = cmd_args.input
        input_ext = os.path.splitext(input_str)[1]

        try:
            inputs = set()
            self.parse_input(input_str, inputs)

            for algorithm_path in inputs:
                self.run_for_file(algorithm_path, cmd_args, result_series)

        except KeyboardInterrupt:
            log.info("Stopped")
        finally:
            TextReport(cmd_args.seconds).generate(result_series)


class ArgumentParser(argparse.ArgumentParser):
    @staticmethod
    def __epilog():
        return (
            "Run algorithms"
        )

    def __init__(self):
        super().__init__(epilog=self.__epilog())
        self.add_argument("-t", "--target", type=str, help="Target to run on", required=True)

        self.add_argument("input", type=str, help="Path to input file/list")
        self.add_argument("-g", "--seconds", action='store_true', help="Output result in seconds")
        self.add_argument("-cores", "--core-amount", default=1, type=int,
                          help="Number of used cores")

        self.add_argument("--timeout", default=900, type=int, metavar="SECONDS",
                          help="Sets a timeout for algorithm")
        self.add_argument("-wi", "--warmup-iters", default=0, type=int,
                          help="Number of warmup iterations")
        self.add_argument("-mi", "--measure-iters", default=2, type=int,
                          help="Number of measurement iterations")
        self.add_argument("-mt", "--measure-time", default=2, type=int, metavar="SECONDS",
                          help="Time for measuring")
        self.add_argument("-c", "--concurrency", default=1, type=int,
                          help="Number of algorithm possible threads")


if __name__ == "__main__":
    parser = ArgumentParser()
    cmd_args = parser.parse_args()
    ar = AlgorithmRunner(cmd_args.target)
    ar.main(cmd_args)
