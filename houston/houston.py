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
        self.mods = None
        self.regexs = None
        self.conf = utils.conf.Configuration(args)
        self._load_modules()
        self._load_adapters()
        self._load_regexes()

    def _load_adapters(self):
        regex = re.compile(r'(adapter_\w+).py')
        adapters = []
        for fil in os.listdir('adapters'):
            match = regex.match(fil)
            if(match is not None):
                adapter = my_import('adapters.%s' % match.group(1))
                if adapter not in adapters:
                    adapters.append(adapter)
                    print("found adapter %s." % match.group(1))
        self.adapters = adapters

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
        self.mods = mods

    def _load_regexes(self):
        self.regex = []
        for mod in self.mods:
            m = mod.Mod()
            print("Registering %s to %s." % (m.regex, m.respond))
            self.regex.append((m.regex, m.respond))

    def start(self):
        pass


if __name__ == '__main__':
    Houston(sys.argv[1:]).start()
