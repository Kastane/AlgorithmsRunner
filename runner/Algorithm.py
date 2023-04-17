import collections
import os
import re
import log
from report.AlgorithmResult import AlgorithmResult
from GeneratedConfig import GeneratedConfig
from utils import scope_exit

class Algorithm:
    __DIR_PATH = os.path.realpath(os.path.dirname(__file__))
    Params = collections.namedtuple("Params", ['target',
                                               'lang',
                                               'linux_sh',
                                               'algorithm_path',
                                               'framework_dir',
                                               'config',
                                               'timeout',
                                               'js_engine'])

    prm = None

    __platforms = None
    __config_source = None
    __component_patt = re.compile(r'.+' + os.path.sep + 'algorithms' + os.path.sep +
                                  '(?P<component>.+?)' + os.path.sep + '.+')

    def __init__(self):
        self.__generators = {'java': os.path.join(self.__DIR_PATH,
                                                  "config_generators", "JavaGenerator.py"),
                             'js': os.path.join(self.__DIR_PATH,
                                                "config_generators", "JSGenerator.py")}

    @staticmethod
    def __is_runable(file):
        return os.path.isfile(file) and os.access(file, os.X_OK)

    def extract_component(self, algorithm_path):
        m = re.search(self.__component_patt, algorithm_path)
        if not m:
            return None
        return m.group("component")

    def __component(self):
        return self.extract_component(self.prm.algorithm_path)

    def __algorithm_name(self):
        return os.path.basename(self.prm.algorithm_path)

    def __create_result(self, platform, res, comp_time, bin_size):
        component = self.__component()
        algorithm_name = self.__algorithm_name()
        out = getattr(res, "out", None)
        err = getattr(res, "err", None)
        return AlgorithmResult(component, self.prm.config, algorithm_name,
                           out, err, comp_time, bin_size)

    def __create_error_result(self, error_message):
        component = self.__component()
        algorithm_name = self.__algorithm_name()

        new_out = error_message
        new_err = error_message

        return AlgorithmResult(component, self.prm.config, algorithm_name,
                           new_out, new_err, -1.0, -1.0)

    def run_algorithm(self, platform, times=1):
        component = self.__component()
        algorithm_name = self.__algorithm_name()

        print(algorithm_name + " ...", end='\r')
        monitor_data = {}

        res = None
        comp_time = None
        bin_size = None

        with \
                GeneratedConfig(self.prm.config, self.prm.algorithm_path, self.prm.lang), \
                scope_exit(lambda: platform.cleanup()):
            try:
                platform.pre_action()
                res = platform.prepare()
                comp_time = res.compile_time
                bin_size = res.result_size

            except KeyboardInterrupt as e:
                raise e
            except BaseException as e:
                log.exception()

                return [self.__create_error_result(str(e))]

            exception_mes = None
            res_arr = []

            try:
                for _ in range(times):
                    res = platform.run()

                    if res.ret != 0 and res.ret is not None:
                        res.out = "Error: {} -{}".format(os.path.splitext(algorithm_name)[0], res.ret)
                    res_out = getattr(res, "out")
                    res_arr.append(res)
                platform.post_action()

            except KeyboardInterrupt as e:
                raise e

            except BaseException as e:
                log.exception()
                exception_mes = str(e)

            if exception_mes:
                ret = [self.__create_error_result(exception_mes) for _ in res_arr]
            else:
                ret = [self.__create_result(platform, res, comp_time, bin_size) for res in res_arr]

                # Iteration results
                for num, res in enumerate(res_arr, start=1):
                    out = getattr(res, "out", None)
                    log.info("Algorithm run {}/{} output\n{}".format(num, len(res_arr), out), num == 1)

        return ret
