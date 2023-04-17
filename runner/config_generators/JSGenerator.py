from config_generators.BaseGenerator import BaseGenerator


class ConfigGenerator(BaseGenerator):

    def __init__(self, cfg):
        super().__init__(cfg)
        cfg['_tags'] = ""
        cfg['_rank'] = ""
        if cfg['target'] in ('pandajshost', 'jslwdevice',
                             'jsgenhost', 'jsgendevice',
                             'pandaeshost', 'pandaesdevice'):
            self.ext = ".js"
            self.unit = 'var benchmarkConfig = {'
            self.prefix = ""
            self.eol = "};\n"
        else:
            self.ext = ".c"
            self.unit = '#include "header.h"\n' +\
                        "struct BaseConfig baseConfig = {"
            self.prefix = ""
            self.eol = ";\n"

    def get_param_types(self):
        for param, val in self.cfg.items():
            if type(val) is str:
                typ = "char *"
                val = '"' + val + '"'
            elif type(val) is int:
                typ = "int"
            elif type(val) is float:
                typ = "float"
            elif type(val) is bool:
                typ = "bool"
            else:
                raise Exception("Invalid config")
            self.cfg[param] = (typ, val)
