"""
This is the main conf module for Houston. IT checks for values in multiple places:
 * Env vars
 * cli options
 * json-style or ini-style file conf
"""

import json
import os

class Configuration:

    def __init__(self, cli_args=None):
        self.json = None
        self.ini = None
        self.args = cli_args

    def get_value(self, key):
        value = self._get_value_cli(key)
        if(value is not None):
            return value
        value = self._get_value_env(key)
        if(value is not None):
            return value
        value = self._get_value_json(key)
        if(value is not None):
            return value
        value = self._get_value_ini(key)
        if(value is not None):
            return value
        return None


    def _get_value_json(self, key):
        if(self.json is not None):
            found_key = None
            if( key in self.json):
                return self.json[key]
            # TODO: find a convenient way to walk trought all the json tree

        else:
            return None

    def _get_value_env(self, key):
        if(key in os.environ):
            return os.environ[key]

    def _get_value_cli(self, key):

        # TODO: use argparse

        # if(self.args is not None):
        #     i = 1
        #     for arg in self.args:
        #         if(arg == '--%s' % key)

    def _parse_json_file(self, file_name):
        try:
            data = ""
            with open(file_name, 'r') as f:
                data = f.read()
            self.json = json.loads(data)
            if( self.get_value("debug") is not None and self.get_value("verbosity") >=1):
                print("JSON config from file %s:\n%s" % (file_name, json.dumps(self.json)))

        except e:
            self.json = False

    def _parse_ini_file(self, file):
        pass
