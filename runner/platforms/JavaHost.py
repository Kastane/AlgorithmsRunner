from platforms.PlatformBase import PlatformBase
from platforms.auxiliary.Misc import Misc
import platforms.auxiliary.JavaUtils as ju
import os


class Platform(PlatformBase):
    framework_name = "Framework.jar"

    def __init__(self, prm):
        super(Platform, self).__init__(prm)
        self._ext_units = []
        ju.init(self)

        # Save possible artifacts to remove them at the end
        self.artifacts['host'].append(os.path.join(self.algorithm_dirname, 'GeneratedConfig.java'))
        self.artifacts['host'].append(os.path.join(self.algorithm_dirname, '*.class'))

    def prepare(self):
        self._compilers.javac_build(self._unit)
        self._compilers.build_native_host(self.algorithm_dirname, self._unit)
        # Extra build
        ju.ext_javac_build(self)
        ju.ext_jar_pack(self)
        return self._unit

    def run(self):
        if self._unit.unit_type != 'class':
            raise Exception("run: unit.type is not 'class' ({})".format(self._unit.unit_type))
        runtime = "java "

        cp = []

        if type(self._unit.unit) == str:
            cp.append(os.path.dirname(self._unit.unit))
        elif type(self._unit.unit) == list:
            for item in self._unit.unit:
                cp.append(os.path.dirname(item))

        cp.append(self.framework_path)

        run_cmd = Misc.measure_cmd.format("{} -cp {} {}".format(
            runtime,
            ":".join(set(cp)),
            Misc.fw_entrypoint),
            Misc.local_tmp_path)

        result = self.execute_algorithm(self.prm.linux_sh, run_cmd)
        return result