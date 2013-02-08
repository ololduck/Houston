"""
Base shell adapter.
"""

import sys

ADAPTER_ID_STRING = "adapter_shell"
NAME = "Shell Default adapter"
VERSION_STRING = "0.1.0"


class Adapter:
    """docstring for Adapter"""

    def __init__(self, conf):
        if(conf is not None):
            self.conf = conf
        else:
            raise Exception("%s: No configuration given" % NAME)

        self.data_available = False
        self.data = ""

    def _read(self):
        d = self.data
        self.data = ""
        # print("Was '%s' is now '%s'" % (d, self.data))
        self.data_available = False
        return d

    def read(self):
        return {"sender": "shell", "full_message": self._read()}

    def send(self, msg, to=None):
        print(msg)

    def loop(self):
        while True:
            self.data += raw_input("%s> " % self.conf["bot_name"])
            self.data_available = True
            sys.stdin.flush()

    def start(self):
        self.loop()

    def get_id_info(self):
        return (NAME, ADAPTER_ID_STRING, VERSION_STRING)
