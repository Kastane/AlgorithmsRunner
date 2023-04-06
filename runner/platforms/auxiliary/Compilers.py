import shutil
import os
import glob
import re
from Colors import Colors

ALL_COMPILERS = ('javac')


class Compilers:
    class Unit:
        def __init__(self):
            self.result = None
            self.unit_type = None
            self.unit = None
            self.out_dir = None
            self.compile_time = 0
            self.measure_time = True
            self.result_size = 0
            self.env = {}

        def update_values(self, res, size, unit_type, unit):
            self.result = res.ret
            self.compile_time += res.tm
            self.result_size = size
            self.unit_type = unit_type
            self.unit = unit
            self.measure_time = True

    native_dir = "native"
    native_libs = os.path.join(native_dir, "*.so")

    def __init__(self, sh, debug=False):
        self.__debug = debug
        self.__sh = sh

    def __dbg_print(self, msg):
        if self.__debug:
            print("[Compilers] " + msg)

    def __unglob_unit(self, unit):
        if type(unit.unit) == str:
            tmp = unit.unit
            unit.unit = glob.glob(unit.unit)
            if not unit.unit:
                raise Exception(unit.unit_type + " : There is no such files '{}'".format(tmp))
        elif type(unit.unit) == list:
            tmp = []
            for elem in unit.unit:
                tmp += glob.glob(elem)
            if not tmp:
                raise Exception(unit.unit_type + " : There is no such files '{}'".format(
                                ", ".join(unit.unit)))
            unit.unit = tmp
        else:
            raise Exception(unit.unit_type + " : unsupported unit.unit type '{}'".format(
                            type(unit.unit)))

    def get_tool_version(self, tool):
        if 'javac' == tool:
            return self.__sh.grep_output('javac -version', r'javac ([0-9\._]+)')
        else:
            return '???'

    def get_compilers(self):
        compilers = []
        for c in ALL_COMPILERS:
            v = self.get_tool_version(c)
            if v is not None:
                compilers.append({c: v})
        return compilers

    def javac_build(self, unit):
        # Env setup to start working
        if unit.unit_type != 'java':
            raise Exception("javac: Unit type is not java")

        if not shutil.which("javac"):
            raise Exception("javac: There is no javac in PATH")

        self.__unglob_unit(unit)
        cp = ""

        if 'cp' in unit.env or 'fw_path' in unit.env:
            cp = "-cp " + unit.env['cp'] + ":" + unit.env['fw_path']

        if unit.out_dir:
            out_dir = "-d " + unit.out_dir
            for cl in glob.glob(os.path.join(unit.out_dir, "*.class")):
                os.remove(cl)
        else:
            out_dir = ""
            # Assume all classes in one dir
            for cl in glob.glob(os.path.join(os.path.dirname(unit.unit[0]), "*.class")):
                os.remove(cl)

        # Compile algorithm sources
        jopts = "-J-XX:+UseParallelGC -J-Xverify:none -J-XX:TieredStopAtLevel=1"
        src = " ".join(unit.unit)
        cmd = "javac {} -source 1.8 -target 1.8 {} {} {}".format(jopts, cp, out_dir, src)
        self.__dbg_print("Run: " + cmd)
        res = self.__sh.run_n_check_result(cmd, measure_time=unit.measure_time)

        if not res or res.ret != 0:
            raise Exception("javac: command '{}' failed ({})", cmd, res)

        if unit.out_dir:
            tmp = unit.out_dir
        else:
            tmp = os.path.dirname(unit.unit[0])
        new_unit = os.path.join(tmp, "*.class")
        size = 0
        for cl in glob.glob(new_unit):
            size += os.path.getsize(cl)

        unit.update_values(res, size, 'class', new_unit)
        return unit

    def build_native_host(self, algorithm_dirname, unit):
        # Check if the algorithm uses native interface
        native_dir = os.path.join(algorithm_dirname, self.native_dir)
        if not os.path.isdir(native_dir):
            return None
        compiler = "gcc"
        possible_include_dirs = ("/usr/lib/jvm/java-8-openjdk-amd64/include",
                                 "/usr/lib/jvm/java-1.8-openjdk/include",
                                 "/usr/lib/jvm/bellsoft-java8-amd64/include")
        include_dir = None
        for d in possible_include_dirs:
            if os.path.isdir(d):
                include_dir = d
                break
        if not include_dir:
            return None
        
        algorithm_name = os.path.basename(os.path.dirname(algorithm_dirname))

        src_file = os.path.join(algorithm_dirname, "native", algorithm_name + ".cc")
        out_file = os.path.join(algorithm_dirname, "native", "lib" + algorithm_name + ".so")
        res = self.__sh.run(compiler + " -rdynamic -I" + include_dir + " -I" +
                            os.path.join(include_dir, "linux") + " " +
                            src_file + " -shared -o " + out_file + " -fpic",
                            measure_time=True)
        if res.ret == 0:
            u = Compilers.Unit()
            u.update_values(res, os.path.getsize(out_file), 'host_so', out_file)
            self.save_step(u, 'gcc')
            return u
        else:
            raise Exception(f'Build native host failed for {algorithm_dirname}')