# Houston / modules

## Available modules

There are none (for now :3)

## How to create a module

Just create a file in `modules/` with the name `[MOD_ID_STRING].py`, where `MOD_ID_STRING` is the identifiant of your mod. For instance, the `MOD_ID_STRING` of the example mod is `mod_base`, so the resulting filename is `modules/mod_base.py` Please be aware that every `MOD_ID_STRING` should begin by `mod_`. Otherwise, they will not be loaded.

Here is the content of the base mod:

    # -*- conding:utf-8 -*-

    """
    This is the base module from whom every module should inherit.
    """

    MOD_ID_STRING = "mod_base"
    VERSION_STRING = "1.0.0"
    NAME = "Base Mod"


    class Mod:
        """docstring for Mod"""
        def __init__(self, name, conf=None):
            self.bot_name = name
            self.regex = [
                ['hi, %s' % self.bot_name, self._reply_hi],
                ['how old are you\?', self._return_age]
            ]
            if(conf is None):
                raise Exception("No configuration recieved. Aborting %s initialisation" % NAME)
            self.conf = conf

        def _reply_hi(self, msg):
            return "Hello, %s!" % msg['sender']

        def _return_age(self, msg):
            return "I am %s years old." % str(self.conf['age'])

        def get_id_info(self):
            return (NAME, MOD_ID_STRING, VERSION_STRING)

There are a few mandatory things your module must have in order to be loaded/don't mess up the whole thing:

 * the `__init__`fuction must take two parameters: `name`, which is the bot name,and the module configuration, which is in JSON format, in `conf/MOD_ID_STRING.json`.
 * this `self.regex` class attribute, in the flollowing format:

        [
            ["regex of the message", function_to_call],
            ["other regex", other_function_to_call]
        ]

    it will be used to parse the recieved messages and send it to the appropritate function.
 * last, a `get_id_info` function , copy-pasted from above.
