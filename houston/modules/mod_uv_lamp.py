# -*- conding:utf-8 -*-

"""
This is the base module from whom every module should inherit.
"""

MOD_ID_STRING = "mod_uv"
VERSION_STRING = "0.0.1"
NAME = "UV Module to control the UV lamp"

import re
import threading


class Mod:
    """docstring for Mod"""
    def __init__(self, conf=None):
        self.bot_name = conf["bot_name"]
        self.regex = [
            [r'^%s, uv (\d{1,3}) ((minutes?)|(seconds))$' % self.bot_name, self._turn_on_uv],
        ]
        if(conf is None):
            raise Exception(
                "No configuration recieved. Aborting %s initialisation" % NAME)
        self.conf = conf

    def _turn_on_uv(self, msg):
        r = re.compile('^%s, uv (\d{1,3}) ((minutes?)|(seconds))$' % self.bot_name)
        match = r.match(msg["full_message"])
        time_in_s = 0
        if(match):
            d = "Turning ON UV for %s %s" % (match.group(1), match.group(2))
            if(match.group(2) == 'minute' or match.group(2) == 'minutes'):
                time_in_s = int(match.group(1)) * 60
            else:
                time_in_s = int(match.group(1))
            t = threading.Timer(float(time_in_s), self._send_uv_end_notice, [msg])
            t.start()
            msg["full_message"] = d
            from_ = msg["from"]
            msg["from"] = msg["to"]
            msg["to"] = from_
            return msg
        else:
            d = ""

    def _send_uv_end_notice(self, orig_msg):
        orig_msg["full_message"] = "UV exposure is over"
        from_ = orig_msg["from"]
        orig_msg["from"] = orig_msg["to"]
        orig_msg["to"] = from_
        orig_msg["interface"].send(orig_msg)

    def get_id_info(self):
        return (NAME, MOD_ID_STRING, VERSION_STRING)
