import os
from tempfile import gettempdir
from Colors import Colors


class Misc:
    rss_out_name = "rss.out"
    rss_out_path = "{{}}/{}".format(rss_out_name)
    local_tmp_path = (
        os.environ.get('TEST_LOCAL_TMP') or gettempdir()).rstrip('/')
    local_rss_path = os.path.join(local_tmp_path, rss_out_name)
    measure_cmd = "\\time -v {{}} 2> {{}}/{}".format(rss_out_name)
    fw_entrypoint = "Starter"