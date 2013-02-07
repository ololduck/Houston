#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os
import re

import utils.conf


class Houston:
    """Main Houston class"""
    def __init__(self, args):
        self.adapters = None
        self.mods = []
        self.conf = utils.conf.Configuration(args)
        self._load_modules()

    def _load_adapters(self):
        pass

    def _load_modules(self):
        regex = re.compile(r'(mod_\w+).py')
        mods = []
        for fil in os.listdir('modules'):
            match = regex.match(fil)
            if(match is not None):
                print("found module %s." % match.group(1))
                mod = __import__('modules.%s' % match.group(1))
                print mod
                mods.append(mod)
                # print(mods[0].Mod)
        print mods

    def start(self):
        pass


if __name__ == '__main__':
    Houston(sys.argv[1:]).start()
