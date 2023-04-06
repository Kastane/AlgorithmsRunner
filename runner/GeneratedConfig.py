import os

from utils import import_module


class GeneratedConfig:

    __DIR_PATH = os.path.realpath(os.path.dirname(__file__))

    __GENERATORS = {
        'java': os.path.join(__DIR_PATH, "config_generators", "JavaGenerator.py")
    }

    def __init__(self, cfg, algorithm_path, lang, cleanup=True):
        self.cfg, self.algorithm_path, self.lang = cfg, algorithm_path, lang
        self.config_source = None
        self._cleanup = cleanup

    def create(self):
        if self.lang in self.__GENERATORS:
            self.cfg['className'] = os.path.splitext(os.path.basename(self.algorithm_path))[0]
            generator_module = import_module("generator", self.__GENERATORS[self.lang])
            generator = generator_module.ConfigGenerator(self.cfg)
            filename, code = generator.generate()
            self.config_source = os.path.join(os.path.dirname(self.algorithm_path), filename)

            with open(self.config_source, 'w') as f:
                f.write(code)

        return self

    def cleanup(self):
        if self.lang not in self.__GENERATORS:
            return
        if os.path.exists(self.config_source):
            os.remove(self.config_source)

    def __enter__(self):
        return self.create()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._cleanup:
            return self.cleanup()
