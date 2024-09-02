# -*- coding: utf-8 -*-


from sys import argv
from urllib.parse import unquote_plus

from iapc import Client
from iapc.tools import containerUpdate, getAddonId, playMedia


__plugin_url__ = f"plugin://{getAddonId()}"


# selectInstance ---------------------------------------------------------------

def selectInstance():
    return Client().instance.selectInstance()


# selectRegion -----------------------------------------------------------------

def selectRegion():
    return Client().instance.selectRegion()


# playFromYouTube --------------------------------------------------------------

__fromYoutube_url__ = f"{__plugin_url__}/?action=play&yt=true&videoId={{}}"

def playFromYouTube(videoId):
    playMedia(__fromYoutube_url__.format(videoId))


# playWithYouTube --------------------------------------------------------------

__withYoutube_url__ = "plugin://plugin.video.youtube/play/?incognito=true&video_id={}"

def playWithYouTube(videoId):
    playMedia(__withYoutube_url__.format(videoId))


# goToChannel ------------------------------------------------------------------

__channel_url__ = f"{__plugin_url__}/?action=channel&channelId={{}}"

def goToChannel(channelId):
    containerUpdate(__channel_url__.format(channelId))


# feed -------------------------------------------------------------------------

def addChannelToFeed(channelId):
    return Client().feed.addChannel(channelId)

def removeChannelFromFeed(channelId):
    return Client().feed.removeChannel(channelId)

def clearChannelsFromFeed():
    return Client().feed.clearChannels()


# search -----------------------------------------------------------------------

def updateQueryType(q):
    return Client().search.updateQueryType(q)

def updateQuerySort(q):
    return Client().search.updateQuerySort(q)

def removeQuery(q):
    return Client().search.removeQuery(q)

def clearHistory():
    return Client().search.clearHistory()


# __main__ ---------------------------------------------------------------------

__scripts__ = {
    "selectInstance": selectInstance,
    "selectRegion": selectRegion,
    "playFromYouTube": playFromYouTube,
    "playWithYouTube": playWithYouTube,
    "goToChannel": goToChannel,
    "addChannelToFeed": addChannelToFeed,
    "removeChannelFromFeed": removeChannelFromFeed,
    "clearChannelsFromFeed": clearChannelsFromFeed,
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
