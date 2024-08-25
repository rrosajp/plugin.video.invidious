# -*- coding: utf-8 -*-


from sys import argv
from urllib.parse import unquote

from iapc import Client

from invidious.regional import selectRegion


# selectInstance ---------------------------------------------------------------

def selectInstance():
    return Client().selectInstance()


# __main__ ---------------------------------------------------------------------

__scripts__ = {
    "selectRegion": selectRegion,
    "selectInstance": selectInstance
}

def dispatch(name, *args):
    if (not (script := __scripts__.get(name)) or not callable(script)):
        raise Exception(f"Invalid script '{name}'")
    script(*(unquote(arg) for arg in args))


if __name__ == "__main__":
    dispatch(*argv[1:])
