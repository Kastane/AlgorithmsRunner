class BaseGenerator:

    unit = ""
    prefix = ""
    eol = ""
    cfg = None
    filename = "GeneratedConfig"
    ext = ""
    base_params = ("className",
                   "threadAmount",
                   "measureIters",
                   "measureTime",
                   "warmupIter",
                   "workDir")

    def __init__(self, cfg):
        self.cfg = cfg.copy()
        self.get_param_types()

    def generate(self):
        if (self.ext == ".java"):
            fields = []
            assignments = []
            for name, (typ, val) in self.cfg.items():
                if name in self.base_params:
                    assignments.append(name + " = " + self.formatted(typ, val) + self.eol)
                else:
                    fields.append(self.prefix + typ + " " + name + " = " +
                                  self.formatted(typ, val) + self.eol)

            code = self.unit.format("".join(fields), "".join(assignments))

        return self.filename + self.ext, code

    def get_param_types(self):
        pass

    def formatted(self, typ, val):
        return str(val).lower() if typ == "boolean" else str(val)  # true/false, not True/False
