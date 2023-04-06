from contextlib import contextmanager
from importlib.util import spec_from_file_location, module_from_spec
from typing import Callable


def import_module(module_name, path):
    spec = spec_from_file_location(module_name, path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@contextmanager
def scope_exit(on_exit: Callable):
    try:
        yield None
    finally:
        on_exit()
