#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os
import re

import utils.conf


def my_import(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod


class Houston:
    """Main Houston class"""
    def __init__(self, args):
        self.adapters = None
        self.mods = []
        self.conf = utils.conf.Configuration(args)
        self._load_modules()
        self._load_adapters()

    def _load_adapters(self):
        regex = re.compile(r'(adapter_\w+).py')
        adapters = []
        for fil in os.listdir('adapters'):
            match = regex.match(fil)
            if(match is not None):
                print("found adapter %s." % match.group(1))
                adapter = my_import('adapters.%s' % match.group(1))
                if adapter not in adapters:
                    adapters.append(adapter)

    def _load_modules(self):
        regex = re.compile(r'(mod_\w+).py')
        mods = []
        for fil in os.listdir('modules'):
            match = regex.match(fil)
            if(match is not None):
                mod = my_import('modules.%s' % match.group(1))
                if mod not in mods:
                    mods.append(mod)
                    print("found module %s." % match.group(1))

    def start(self):
        pass


if __name__ == '__main__':
    Houston(sys.argv[1:]).start()
