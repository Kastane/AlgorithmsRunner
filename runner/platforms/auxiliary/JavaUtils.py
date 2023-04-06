import os
from platforms.auxiliary.Misc import Misc


def init(platform):
    # Check for framework
    jar_targets = ["javahost", "javadevice"]

    platform.framework_path = os.path.join(platform.prm.framework_dir,
                                           platform.prm.lang,
                                           platform.framework_name)
    check_framework(platform.framework_path)

    algorithm_dirname = platform.algorithm_dirname

    if platform.prm.target in jar_targets:
        platform.bytecode_dir_path = os.path.join(
                    "{}".format(algorithm_dirname), "out", "jars")

    platform._unit.unit = [os.path.join(platform.algorithm_dirname, "*.java")]
    platform._unit.unit_type = 'java'
    platform._unit.env['cp'] = ""
    platform._unit.env['result_name'] = platform._get_class_name()
    platform._unit.env['fw_path'] = platform.framework_path
    platform._unit.out_dir = platform.algorithm_dirname


def check_framework(framework_path):
    if not os.path.isfile(framework_path):
        print("Framework not found. Search path:", framework_path)
        exit(1)


def ext_javac_build(platform):
    ext_path = os.path.join(platform.algorithm_dirname, "ext")
    if os.path.exists(ext_path):
        # Initialize extra units and compile them
        for ext_d in os.listdir(ext_path):
            ext_unit = platform._compilers.Unit()
            ext_unit.unit_type = 'java'
            ext_unit.unit = os.path.join(ext_path, ext_d, "*.java")
            ext_unit.env['result_name'] = ext_d
            ext_unit.env['fw_path'] = platform.framework_path
            ext_dst_dir = os.path.join(platform.algorithm_dirname, "out", "classes", ext_d)
            if not os.path.exists(ext_dst_dir):
                os.makedirs(ext_dst_dir)
            ext_unit.out_dir = ext_dst_dir
            ext_unit.env['cp'] = platform.prm.host_class_path
            platform._ext_units.append(ext_unit)
            platform._compilers.javac_build(ext_unit)


def ext_jar_pack(platform):
    if platform._ext_units:
        ext_jar_dst_dir = os.path.join(platform.algorithm_dirname, "out", "jars")
        if not os.path.exists(ext_jar_dst_dir):
            os.makedirs(ext_jar_dst_dir)
        for ext_unit in platform._ext_units:
            ext_unit.out_dir = ext_jar_dst_dir
            platform._compilers.jar_pack(ext_unit)
