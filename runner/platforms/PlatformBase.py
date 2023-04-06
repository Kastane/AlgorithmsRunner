import log
import importlib.util

from platforms.auxiliary.Compilers import Compilers
from platforms.auxiliary.Misc import Misc

import os


class PlatformBase:
    __debug = None

    native_dir = Compilers.native_dir
    native_libs = Compilers.native_libs

    def _check_type(self, unit, unit_type):
        if isinstance(unit_type, list):
            if unit.unit_type not in unit_type:
                raise Exception(
                    "TypeError",
                    f"unit.type isn't in {unit_type} ({unit.unit_type})"
                )
            else:
                return

        if unit.unit_type != unit_type:
            raise Exception("TypeError", "unit.type isn't {} ({})".format(unit_type,
                                                                          unit.unit_type))

    def __init__(self, prm):
        self.prm = prm
        self.framework_path = self.prm.framework_dir
        self.algorithm_dirname = os.path.dirname(self.prm.algorithm_path)
        self.algorithm_name = os.path.splitext(os.path.basename(self.prm.algorithm_path))[0]
        self.artifacts = {'host': []}
        self._compilers = Compilers(self.prm.linux_sh)
        self._unit = Compilers.Unit()

    def __action(self, action_name):
        action_script = os.path.join(self.algorithm_dirname, "host_" + action_name + ".py")

        if os.path.isfile(action_script):
            spec = importlib.util.spec_from_file_location(action_name, action_script)
            action_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(action_module)
            action = action_module.Action(self)
            action.run()

    def pre_action(self):
        self.__action("pre_action")

    def post_action(self):
        self.__action("post_action")

    def _get_class_name(self):
        class_name = os.path.basename(self.prm.algorithm_path)
        class_name = os.path.splitext(class_name)[0]
        return class_name

    def prepare(self):
        pass

    def run(self):
        pass

    def execute_algorithm(self, shell, cmd, **kwargs):
        return shell.run_with_config(cmd, False)

    def print_debug_info(self):
        """Print platform-dependent info, if any, that can be helpful in diagnosing failures"""
        pass  

    def cleanup(self):
        pass
        for artifact in self.artifacts['host']:
            self.prm.linux_sh.run("rm -rf " + artifact)

