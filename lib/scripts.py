# -*- coding: utf-8 -*-


from sys import argv
from urllib.parse import unquote_plus

from iapc import Client
from iapc.tools import containerUpdate, getAddonId


__plugin_url__ = f"plugin://{getAddonId()}"


# selectInstance ---------------------------------------------------------------

def selectInstance():
    return Client().instance.selectInstance()


# selectRegion -----------------------------------------------------------------

def selectRegion():
    return Client().instance.selectRegion()


# goToChannel ------------------------------------------------------------------

__channel_url__ = f"{__plugin_url__}/?action=channel&channelId={{}}"

def goToChannel(channelId):
    containerUpdate(__channel_url__.format(channelId))


# updateQueryType --------------------------------------------------------------

def updateQueryType(q):
    return Client().search.updateQueryType(q)


# updateQuerySort --------------------------------------------------------------

def updateQuerySort(q):
    return Client().search.updateQuerySort(q)


# removeQuery ------------------------------------------------------------------

def removeQuery(q):
    return Client().search.removeQuery(q)


# clearHistory -----------------------------------------------------------------

def clearHistory():
    return Client().search.clearHistory()


# __main__ ---------------------------------------------------------------------

__scripts__ = {
    "selectInstance": selectInstance,
    "selectRegion": selectRegion,
    "goToChannel": goToChannel,
    "updateQueryType": updateQueryType,
    "updateQuerySort": updateQuerySort,
    "removeQuery": removeQuery,
    "clearHistory": clearHistory
}

def dispatch(name, *args):
    if (not (script := __scripts__.get(name)) or not callable(script)):
        raise Exception(f"Invalid script '{name}'")
    script(*(unquote_plus(arg) for arg in args))


if __name__ == "__main__":
    dispatch(*argv[1:])
