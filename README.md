# Houston

Houston is a automation bot, centered around a plugin system. It will have multiple adapters, simple interfaces that control a protocol.
All the commands are plugins.

## modules

See [Modules Documentation](houston/modules/README.md).

## Adapters (aka. protocol implementations)

See [Adapter Documentation](houston/adapters/README.md)

## Generic doc

All messages transfered must be a dictionnary with the following format:

    {
        "from": "someguy",
        "to": "someotherguy",
        "room": "some value, make sure it is exact",
        "full_message": "actual human content",
        "interface": used_adapter.__class__
    }
