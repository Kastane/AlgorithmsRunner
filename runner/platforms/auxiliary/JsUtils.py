import os


def init(platform):
    platform._unit.unit = [os.path.join(platform.algorithm_dirname, "*.js")]
    platform._unit.unit_type = 'js'
    platform._unit.out_dir = platform.algorithm_dirname
    platform.framework_dir = os.path.join(platform.prm.framework_dir,
                                          platform.prm.lang)
    platform.framework_path = os.path.join(platform.framework_dir,
                                           platform.framework_name)
    platform.algorithm_name = os.path.basename(platform.prm.algorithm_path)


def get_js_engine_options(engine, mode):
    try:
        return {
            'v8': {'int': '--no-opt --jitless --use-ic'},
            'd8': {'int': '--no-opt --jitless --use-ic'}
            }[engine][mode]
    except Exception:
        pass
    raise Exception(f'Engine {engine} mode {mode} is not implemented!')


def build_js_script(platform, target="host", sh=None):
    """ Concatenate all js files into one script """

    # the separate files to merge
    paths = [os.path.join(platform.framework_dir, "utils/Consumer.js"),
             platform.prm.algorithm_path]
    # the final script
    out_script = os.path.join(platform.algorithm_dirname, "generated.js")

    with open(out_script, 'w') as out:
        for file in paths:
            with open(file) as src:
                out.write(src.read())
            out.write("\n")

    platform._compilers.build_gen_cfg_c(platform._unit, platform.framework_dir,
                                        platform.algorithm_dirname, target=target, sh=sh)
    platform._unit.unit_type = "js+so"
    platform._unit.unit = (platform._unit.unit, out_script)
    return


def compile_benchmark_script(platform, target="host", sh=None):
    # the separate files to merge
    paths = [platform.consumer_path,
             platform.prm.algorithm_path,
             os.path.join(platform.prm.framework_dir, platform.framework_name),
             platform.cfg_path]

    # the final script
    out_script = platform.script_path

    with open(out_script, 'w') as out:
        for file in paths:
            with open(file) as src:
                out.write(src.read())
            out.write("\n")

    # Some JavaScript engines do not provide compile time and bytecode size information
    platform._unit.compile_time = None
    platform._unit.result_size = None

    platform._unit.unit_type = "js+so"
    platform._unit.unit = (platform._unit.unit, out_script)
    return