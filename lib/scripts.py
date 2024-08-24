# -*- coding: utf-8 -*-


from sys import argv
from urllib.parse import unquote

from iapc.tools import playMedia

from invidious.client import IVClient
from invidious.regional import selectRegion


# playWithYouTube --------------------------------------------------------------

__withYoutube_url__ = "plugin://plugin.video.youtube/play/?incognito=true&video_id={}"

def playWithYouTube(videoId):
    playMedia(__withYoutube_url__.format(videoId))


# selectInstance ---------------------------------------------------------------

def selectInstance():
    return IVClient().selectInstance()


# __main__ ---------------------------------------------------------------------

__scripts__ = {
    "playWithYouTube": playWithYouTube,
    "selectRegion": selectRegion,
    "selectInstance": selectInstance
}

def dispatch(name, *args):
    if (not (script := __scripts__.get(name)) or not callable(script)):
        raise Exception(f"Invalid script '{name}'")
    script(*(unquote(arg) for arg in args))


if __name__ == "__main__":
    dispatch(*argv[1:])
