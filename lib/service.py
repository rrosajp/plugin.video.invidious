# -*- coding: utf-8 -*-


from functools import wraps

from iapc import public, Service
from iapc.tools import (
    containerRefresh, getSetting, makeProfile, notify, ICONERROR
)

from invidious.extract import (
    IVChannel, IVChannelPlaylists, IVChannelVideos, IVPlaylistVideos, IVVideo
)
from invidious.folders import home
from invidious.instance import IVInstance
from invidious.search import IVSearch


# cached -----------------------------------------------------------------------

def cached(name):
    def decorator(func):
        @wraps(func)
        def wrapper(self, key, *args, **kwargs):
            cache = self.__cache__.setdefault(name, {})
            if (not (value := cache.get(key))):
                value = cache[key] = func(self, *(args or (key,)), **kwargs)
            return value
        return wrapper
    return decorator


# ------------------------------------------------------------------------------
# IVService

class IVService(Service):

    def __init__(self, *args, **kwargs):
        super(IVService, self).__init__(*args, **kwargs)
        makeProfile()
        self.__instance__ = IVInstance(self.logger)
        self.__search__ = IVSearch(self.logger, self.__instance__)
        self.__cache__ = {}

    def __setup__(self):
        self.__instance__.__setup__()
        self.__search__.__setup__()

    def start(self, **kwargs):
        self.logger.info("starting...")
        self.__setup__()
        self.serve(**kwargs)
        self.logger.info("stopped")

    def onSettingsChanged(self):
        self.__setup__()
        containerRefresh()

    # --------------------------------------------------------------------------

    def __raise__(self, error, throw=True):
        if not isinstance(error, Exception):
            error = Exception(error)
        notify(f"error: {error}", icon=ICONERROR)
        if throw:
            raise error

    # play ---------------------------------------------------------------------

    @public
    def play(self, **kwargs):
        self.logger.info(f"play(kwargs={kwargs})")
        if (videoId := kwargs.pop("videoId")):
            return IVVideo(self.__instance__.request("video", videoId))
        self.__raise__("Missing videoId", throw=False)

    # channel ------------------------------------------------------------------

    @cached("channels")
    def __channel__(self, channelId):
        return IVChannel(self.__instance__.request("channel", channelId))

    @public
    def channel(self, **kwargs):
        self.logger.info(f"channel(kwargs={kwargs})")
        if (channelId := kwargs.pop("channelId")):
            return self.__channel__(channelId)
        self.__raise__("Missing channelId", throw=False)

    @public
    def tabs(self, **kwargs):
        self.logger.info(f"tabs(kwargs={kwargs})")
        if (channelId := kwargs.pop("channelId")):
            return self.__channel__(channelId)["tabs"]
        self.__raise__("Missing channelId", throw=False)

    def __tab__(self, key, **kwargs):
        self.logger.info(f"__tab__(key={key}, kwargs={kwargs})")
        if (channelId := kwargs.pop("channelId")):
            return (
                self.__channel__(channelId)["channel"],
                self.__instance__.request(key, channelId, **kwargs)
            )
        self.__raise__("Missing channelId", throw=False)

    @public
    def tab(self, key, **kwargs):
        self.logger.info(f"tab(kwargs={kwargs})")
        return IVChannelVideos(*self.__tab__(key, **kwargs))

    @public
    def playlists(self, **kwargs):
        self.logger.info(f"playlists(kwargs={kwargs})")
        return IVChannelPlaylists(*self.__tab__("playlists", **kwargs))


    # playlist -----------------------------------------------------------------

    @public
    def playlist(self, **kwargs):
        self.logger.info(f"playlist(kwargs={kwargs})")
        if (playlistId := kwargs.pop("playlistId")):
            return IVPlaylistVideos(
                self.__instance__.request("playlist", playlistId, **kwargs)
            )
        self.__raise__("Missing playlistId", throw=False)

    # home ---------------------------------------------------------------------

    @public
    def home(self):
        return [
            folder for folder in home
            if (
                getSetting(f"home.{folder['type']}", bool)
                if folder.get("optional", False)
                else True
            )
        ]

    # feed ---------------------------------------------------------------------

    @public
    def feed(self, **kwargs):
        self.logger.info(f"feed(kwargs={kwargs})")


# __main__ ---------------------------------------------------------------------

if __name__ == "__main__":
    service = IVService()
    kwargs = {
        "instance": service.__instance__,
        "search": service.__search__
    }
    service.start(**kwargs)
