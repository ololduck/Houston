"""
This is a Skeleton adapter. It explains the basic structure of an adapter.
"""

ADAPTER_ID_STRING = 'adapter_irc'
NAME = 'irc adapter'
VERSION_STRING = '0.0.1'


class Adapter:
    """docstring for Adapter"""

    def __init__(self, conf):
        if(conf is not None):
            self.conf = conf
        else:
            raise Exception("%s: No configuration given" % NAME)

        self.data_available = False
        self.data = ""

    def read(self):
        return {"sender": "Sender of the message if any", "full_message": "All the message content, without the metadata, like author, time..."}

    def send(self, msg, to=None):
        # Here is the function called when a message needs to be passed.
        pass

    def loop(self):
        # This is the main loop of the adapter. It should probalby try to recieve data, set the self.data_available flag to True, and store the data
        while True:
            pass

    def start(self):
        # This is called to start the adapter. All protocol-specific communication may be done here, before calling self.loop().
        self.loop()

    def get_id_info(self):
        return (NAME, ADAPTER_ID_STRING, VERSION_STRING)
