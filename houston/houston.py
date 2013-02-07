#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os
import re
import json
import threading

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
        self.conf._parse_json_file()
        self._load_adapters()
        self._load_modules()

    def _load_adapters(self):
        regex = re.compile(r'(adapter_\w+).py')
        adapters = []
        for fil in os.listdir('adapters'):
            match = regex.match(fil)
            if(match is not None):
                adapter = my_import('adapters.%s' % match.group(1))
                if adapter not in adapters:
                    adapters.append(adapter)
                    print("Found adapter \'%s\' version %s." % (adapter.NAME, adapter.VERSION_STRING))
        if(self.adapters == []):
            raise Exception("No suitable adapters found!")
        self.adapters = adapters

    def _load_modules(self):
        regex = re.compile(r'(mod_\w+).py')
        mods = []
        self.regexs = []
        for fil in os.listdir('modules'):
            try:
                match = regex.match(fil)
                if(match is not None):
                    mod = my_import('modules.%s' % match.group(1))
                    conf = None
                    with open('conf/%s.json' % mod.MOD_ID_STRING, 'r') as f:
                        conf = json.loads(f.read())
                    m = mod.Mod(self.conf.get_value('bot_name'), conf)
                    if(not self._is_mod_already_present(mods, m)):
                        print("Found module \'%s\' (%s) version %s." % (mod.NAME, mod.MOD_ID_STRING, mod.VERSION_STRING))
                        for r_conf in m.regex:
                            print("Registering '%s' to %s." % (r_conf[0], r_conf[1]))
                            self.regexs += [r_conf, ]
                        mods.append(m)
            except Exception as e:
                print(e)
        if(mods == []):
            raise Exception("No modules found! Remember: i can't do anything without commands!")
        self.mods = mods
        print self.regexs
        for r in self.regexs:
            print(r)
            r[0] = re.compile(r[0])

    def _is_mod_already_present(self, mods, mod):
        for m in mods:
            if(m.__class__ == mod.__class__):
                return True
        return False

    def _load_regexes(self):
        self.regexs = ()
        for mod in self.mods:
            try:
                conf = None
                with open('conf/%s.json' % mod.MOD_ID_STRING, 'r') as f:
                    conf = json.loads(f.read())
                m = mod.Mod(self.conf.get_value('bot_name'), conf)
                for r_conf in m.regex:
                    print("Registering '%s' to %s." % (r_conf[0], r_conf[1]))
                    self.regexs += r_conf
            except Exception as e:
                print(e)

    def run(self):
        adapters = []
        for a in self.adapters:
            adapters.append(a.Adapter(self.conf.json))
        for a in adapters:
            thread = threading.Thread(target=a.start)
            thread.start()
        while True:
            for a in adapters:
                if(a.data_available):
                    data = a.read()
                    for r in self.regexs:
                        match = r[0].match(data["full_message"])
                        if(match):
                            a.send(r[1](data))


if __name__ == '__main__':
    bot = Houston(sys.argv[1:])
    try:
        bot.run()
        bot.conf.save()
    except KeyboardInterrupt:
        pass
