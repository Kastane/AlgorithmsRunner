import sys
import time
import traceback


def __print_formatted(severity, msg):
    timestamp = int(round(time.time() * 1000))
    print("{} {} [Host] - {}".format(timestamp, severity, msg), file=sys.stderr)


def debug(msg, extra_line=False):
    if extra_line:
        print("\n", file=sys.stderr)
    __print_formatted("DEBUG", msg)


def info(msg, extra_line=False):
    if extra_line:
        print("\n", file=sys.stderr)
    __print_formatted("INFO", msg)


def exception():
    (_, value, tb) = sys.exc_info()
    __print_formatted("ERROR", str(value))
    traceback.print_tb(tb, file=sys.stderr)
