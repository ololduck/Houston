"""
This is the main conf module for Houston. IT checks for values in multiple places:
 * Env vars
 * cli options
 * json-style or ini-style file conf
"""

class Configuration:

    def __init__(self):
        pass

    def get_value(self, key):
        pass

    def _parse_json_file(self, file):
        pass

    def _parse_ini_file(self, file):
        pass
