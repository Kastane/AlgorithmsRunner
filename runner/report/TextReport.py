from Colors import Colors

class TextReport:
    def __init__(self, seconds):
        self.__seconds = seconds

    def __print_result_header(self):
        print(Colors.Green + "Algorithm name".ljust(54) + Colors.End +
              ("Time  s/op " if self.__seconds else "Time ns/op ").rjust(13) +
              " | Ext Time sec | RSS max KB | Compile sec | Size bytes")

    def __print_config_header(self):
        print(Colors.Green + "Config".ljust(10) + 
              Colors.End +  "wi | mi | threads |")

    def __print_config(self): 
        print(("").ljust(16) + cfg["warmupIters"] +
              " | " + str(cfg["measureIters"]).rjust(12) +
              " | " + str(cfg["threadAmount"]).rjust(8))

    def __print_result(self, res):
        if res.result_val is not None:
            if self.__seconds:
                spd = "{:13.5f}".format(res.result_val/1000000000)
            else:
                spd = "{:13.2f}".format(res.result_val)
        else:
            spd = "None".rjust(13)

        compile_time = "N/A" if res.time is None else str(round(res.time, 2))
        binary_size = "N/A" if res.bin_size is None else res.bin_size
        
        print(Colors.Green + (res.name + ": ").ljust(54, '.') + Colors.End + spd +
              " | " + str(res.ext_time).rjust(12) +
              " | " + str(res.rss).rjust(8) + "  " +
              " | " + str(compile_time).rjust(7) + "    " +
              " | " + str(binary_size).rjust(7))

    def generate(self, result_series):
        self.__print_result_header()
        for res_arr in sorted(result_series, key=lambda v: v[0].name if v else None):
            res = res_arr[0] if res_arr is not None and len(res_arr) > 0 else None
            self.__print_result(res)
