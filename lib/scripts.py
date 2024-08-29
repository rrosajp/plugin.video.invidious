# -*- coding: utf-8 -*-


from sys import argv
from urllib.parse import unquote

from iapc import Client
from iapc.tools import containerUpdate, getAddonId

from invidious.regional import selectRegion


__plugin_url__ = f"plugin://{getAddonId()}"


# selectInstance ---------------------------------------------------------------

def selectInstance():
    return Client().instance.selectInstance()


# goToChannel ------------------------------------------------------------------

__channel_url__ = f"{__plugin_url__}/?action=channel&channelId={{}}"

def goToChannel(channelId):
    containerUpdate(__channel_url__.format(channelId))


# removeQuery ------------------------------------------------------------------

def removeQuery(q):
    return Client().search.removeQuery(q)


# clearHistory -----------------------------------------------------------------

def clearHistory():
    return Client().search.clearHistory()


# __main__ ---------------------------------------------------------------------

__scripts__ = {
    "selectRegion": selectRegion,
    "selectInstance": selectInstance,
    "goToChannel": goToChannel,
    "removeQuery": removeQuery,
    "clearHistory": clearHistory
}

def dispatch(name, *args):
    if (not (script := __scripts__.get(name)) or not callable(script)):
        raise Exception(f"Invalid script '{name}'")
    script(*(unquote(arg) for arg in args))


if __name__ == "__main__":
    dispatch(*argv[1:])
