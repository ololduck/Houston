"""

irc adapter

It is still a WIP

TODO : make it recover from deconnection

"""

ADAPTER_ID_STRING = 'adapter_irc'
NAME = 'IRC adapter'
VERSION_STRING = '0.1.0'

import socket
import re
import time


class Adapter:
    """docstring for Adapter"""

    def __init__(self, conf):
        if(conf is not None):
            self.conf = conf
        else:
            raise Exception("%s: No configuration given" % NAME)

        self.data_available = False
        self.waiting_data = []

        self.protocol_specific = {
            "^PING": self._pong,
            " :End of /MOTD command\\.": self._join,
            "^ERROR :Closing Link: ": self._stop
        }

        self.go = True

        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def _stop(self):
        self.go = False

    def _send_to_serv(self, line):
        self.irc.send("%s\n" % str(line))

    def _pong(self, msg):
        """Keeps the link alive"""
        self._send_to_serv("PONG %s" % (msg.split()[1]))

    def _join(self, _):
        for chan in self.conf["channels"]:
            if(self.conf["debug"]):
                print("Trying to join channel %s" % chan)
            self._send_to_serv("JOIN %s" % chan)

    def _get_room(self, msg):
        """Obtains sender's name from message"""
        to = msg[msg.find("PRIVMSG ") + 8:msg.find(" :")]
        return to

    def _get_message(self, msg):
        """ Obtains the message from the raw data"""
        message = msg[msg.find(' :') + 2:]
        return message

    def _get_user(self, msg):
        return msg[1:msg.find("!")]

    def read(self):
        if(self.data_available):
            msg = self.waiting_data[0]
            del self.waiting_data[0]
            if(len(self.waiting_data) == 0):
                self.data_available = False
            return {
                "room": self._get_room(msg),
                "to": self._get_room(msg),
                "from": self._get_user(msg),
                "full_message": self._get_message(msg)
            }
        else:
            return None

    def send(self, msg):
        for i in re.split("\r|\n", str(msg["full_message"])):
            for j in range(1 + len(i) / 400):
                self._send_to_serv("PRIVMSG %s :%s" % (msg["room"], i[400 * j:400 * (j + 1)]))

    def loop(self):
        # This is the main loop of the adapter. It should probalby try to recieve data, set the self.data_available flag to True, and store the data
        while self.go:
            data = re.split("\r|\n", self.irc.recv(4096))
            for i in data:
                matched = False
                for j in self.protocol_specific:
                    match = re.search(j, i)
                    if(match):
                        self.protocol_specific[j](i)
                        matched = True
                if(not matched):
                    self.waiting_data.append(i)
                    self.data_available = True
            time.sleep(0.1)
        self.irc.shutdown(socket.SHUT_RDWR)

    def start(self):
        # This is called to start the adapter. All protocol-specific communication may be done here, before calling self.loop().
        if(self.conf["debug"]):
            print("\nConnecting to %s:%s as %s\n" % (self.conf["server"], self.conf["port"], self.conf["bot_name"]))
        self.irc.connect((self.conf["server"], self.conf["port"]))
        self._send_to_serv("NICK %s" % self.conf["bot_name"])
        self._send_to_serv("USER %s %s %s :%s" % ((self.conf["bot_name"], ) * 4))
        self.loop()

    def get_id_info(self):
        return (NAME, ADAPTER_ID_STRING, VERSION_STRING)
