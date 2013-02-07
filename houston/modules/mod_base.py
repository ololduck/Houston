# -*- conding:utf-8 -*-

"""
This is the base module from whom every module should inherit.
"""

class Mod:
    """docstring for Mod"""
    def __init__(self):
        self.regex = r'*'

    def respond(self, msg):
        return "Hello!"
