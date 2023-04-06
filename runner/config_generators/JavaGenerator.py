from config_generators.BaseGenerator import BaseGenerator


class ConfigGenerator(BaseGenerator):

    def __init__(self, cfg):
        super().__init__(cfg)
        self.ext = ".java"
        constructor = "public " + self.filename + " () {{\n" +\
                      "{}" +\
                      "}}\n"
        self.unit = "public class " + self.filename + " extends BaseConfig {{\n" +\
                    "{}" +\
                    constructor +\
                    "}}\n"
        self.prefix = "public "
        self.eol = ";\n"

    def get_param_types(self):
        for param, val in self.cfg.items():
            if type(val) is str:
                typ = "String"
                val = '"' + val + '"'
            elif type(val) is int:
                typ = "int"
            elif type(val) is float:
                typ = "float"
            elif type(val) is bool:
                typ = "boolean"
            elif param != "mask":
                raise Exception("Invalid config")
            self.cfg[param] = (typ, val)
