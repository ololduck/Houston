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
        regex = re.compile(r'^(adapter_\w+).py$')
        adapters = []
        for fil in os.listdir('adapters'):
            match = regex.match(fil)
            if(match is not None):
                adapter = my_import('adapters.%s' % match.group(1))
                if adapter not in adapters:
                    adapters.append(adapter)
                    print("Found adapter \'%s\'(%s) version %s." % (adapter.NAME, adapter.ADAPTER_ID_STRING, adapter.VERSION_STRING))
        if(self.adapters == []):
            raise Exception("No suitable adapters found!")
        self.adapters = adapters

    def _load_modules(self):
        regex = re.compile(r'^(mod_\w+).py')
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
                    if(conf is not None):
                        conf["bot_name"] = self.conf.get_value("bot_name")
                        if(not "debug" in conf or (conf["debug"] is False)):
                            conf["debug"] = self.conf.get_value("debug")
                    m = mod.Mod(conf)
                    if(not self._is_element_already_present(mods, m)):
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
        for r in self.regexs:
            r[0] = re.compile(r[0])

    def _is_element_already_present(self, lst, elem):
        for e in lst:
            if(e.__class__ == elem.__class__):
                return True
        return False

    def run(self):
        adapters = []
        for a in self.adapters:
            conf = None
            with open("conf/" + a.ADAPTER_ID_STRING + ".json", 'r') as f:
                conf = json.loads(f.read())
            if(conf is not None):
                if("disabled" in conf and conf["disabled"] is True):
                    continue
                conf["bot_name"] = self.conf.get_value("bot_name")
                if(conf["debug"] is False):
                    conf["debug"] = self.conf.get_value("debug")
            adapters.append(a.Adapter(conf))
        if(adapters == []):
            raise Exception("No communication Adapters enabled! I can not do anything.")
        for a in adapters:
            print("Starting interface %s(%s) v%s" % a.get_id_info())
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


def gen_adapter_skel(arg=None):
    if(arg is not None):
        with open('adapters/skeleton', 'r') as f:
            with open('adapters/adapter_%s.py' % arg, 'w+') as f1:
                d = f.read()
                d = d.replace("ADAPTER_ID_STRING = 'adapter_skeleton'", "ADAPTER_ID_STRING = 'adapter_%s'" % arg)
                d = d.replace("NAME = 'Skeleton adapter'", "NAME = '%s adapter'" % arg)
                f1.write(d)
    sys.exit()


def gen_module_skel(arg=None):
    pass


def parse_arg_commands(args=()):
    i = 1
    for arg in args[1:]:
        if(arg == "new-adapter"):
            gen_adapter_skel(args[++i])
        elif(arg == "new-module"):
            gen_module_skel(args[++i])
        else:
            i += 1


if __name__ == '__main__':
    parse_arg_commands(sys.argv)
    bot = Houston(sys.argv[1:])
    try:
        bot.run()
        bot.conf.save()
    except KeyboardInterrupt:
        pass
