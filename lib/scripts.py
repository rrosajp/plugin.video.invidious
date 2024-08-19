# -*- coding: utf-8 -*-


from sys import argv
from urllib.parse import unquote

from iapc import Client
from iapc.tools import getSetting, playMedia, selectDialog, setSetting

from invidious.regional import selectRegion


# playWithYouTube --------------------------------------------------------------

__withYoutube_url__ = "plugin://plugin.video.youtube/play/?incognito=true&video_id={}"

def playWithYouTube(videoId):
    playMedia(__withYoutube_url__.format(videoId))


# selectPublicInstance ---------------------------------------------------------

def selectPublicInstance():
    if (instances := Client().selectPublicInstance(sort_by="location,health")):
        uri = getSetting("instance.uri", str)
        keys = list(instances.keys())
        values = list(instances.values())
        preselect = keys.index(uri) if uri in keys else -1
        index = selectDialog(values, heading=40113, preselect=preselect)
        if index >= 0:
            setSetting("instance.uri", keys[index], str)


# __main__ ---------------------------------------------------------------------

__scripts__ = {
    "playWithYouTube": playWithYouTube,
    "selectPublicInstance": selectPublicInstance,
    "selectRegion": selectRegion
}

def dispatch(name, *args):
    if (not (script := __scripts__.get(name)) or not callable(script)):
        raise Exception(f"Invalid script '{name}'")
    script(*(unquote(arg) for arg in args))


if __name__ == "__main__":
    dispatch(*argv[1:])
