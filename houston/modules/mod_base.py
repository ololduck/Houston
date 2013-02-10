# -*- conding:utf-8 -*-

"""
This is the base module from whom every module should inherit.
"""

MOD_ID_STRING = "mod_base"
VERSION_STRING = "1.0.0"
NAME = "Base Mod"


class Mod:
    """docstring for Mod"""
    def __init__(self, conf=None):
        self.bot_name = conf["bot_name"]
        self.regex = [
            ['(hi)|(hello)(, %s)?' % self.bot_name, self._reply_hi],
            ['how old are you\?', self._return_age]
        ]
        if(conf is None):
            raise Exception("No configuration recieved. Aborting %s initialisation" % NAME)
        self.conf = conf

    def _reply_hi(self, msg):
        return "Hello, %s!" % msg['sender']

    def _return_age(self, msg):
        return "I am %s years old." % str(self.conf['age'])

    def get_id_info(self):
        return (NAME, MOD_ID_STRING, VERSION_STRING)
