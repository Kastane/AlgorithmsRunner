from platforms.PlatformBase import PlatformBase
from platforms.auxiliary.Misc import Misc
import platforms.auxiliary.JsUtils as ju
import os


class Platform(PlatformBase):
    framework_name = "host/Framework.out"

    def __init__(self, prm):
        super(Platform, self).__init__(prm)
        self._ext_units = []
        ju.init(self)

        # Save possible artifacts to remove them at the end
        self.artifacts['host'].append(os.path.join(self.algorithm_dirname, '*.so'))
        self.artifacts['host'].append(os.path.join(self.algorithm_dirname, 'GeneratedConfig.c'))
        self.artifacts['host'].append(os.path.join(self.algorithm_dirname, 'generated.js'))
        self.script_name = 'generated.js'

    def prepare(self):
        ju.build_js_script(self)
        self._unit.compile_time = 0
        return self._unit

    def run(self):
        if self._unit.unit_type != 'js+so':
            raise Exception("run: unit.type is not 'js' ({})".format(self._unit.unit_type))

        os.chdir(self.algorithm_dirname)
        ld_dir = "LD_LIBRARY_PATH={} ".format(self.algorithm_dirname)

        launch_command = "{} {}".format(self.framework_path, self.script_name)
        run_cmd = ld_dir + Misc.measure_cmd.format(launch_command, Misc.local_tmp_path)
        result = self.execute_algorithm(self.prm.linux_sh, run_cmd)
        return result
