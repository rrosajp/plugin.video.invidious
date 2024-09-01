# -*- coding: utf-8 -*-


from functools import wraps

from iapc import public, Service
from iapc.tools import containerRefresh, getSetting, makeProfile

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
            if ((value := cache.get(key)) is None):
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

    # play ---------------------------------------------------------------------

    @public
    def play(self, videoId=None, **kwargs):
        self.logger.info(f"play(videoId={videoId}, kwargs={kwargs})")
        if videoId:
            return IVVideo(self.__instance__.request("video", videoId))
        self.logger.error(f"Invalid videoId: {videoId}", notify=True)

    # channel ------------------------------------------------------------------

    @cached("channels")
    def __channel__(self, channelId):
        self.logger.info(f"__channel__({channelId})")
        if channelId:
            return IVChannel(self.__instance__.request("channel", channelId))
        self.logger.error(f"Invalid channelId: {channelId}", notify=True)

    @public
    def channel(self, channelId=None):
        self.logger.info(f"channel(channelId={channelId})")
        return self.__channel__(channelId)

    @public
    def tabs(self, channelId=None, **kwargs):
        self.logger.info(f"tabs(channelId={channelId}, kwargs={kwargs})")
        if (channel := self.__channel__(channelId)):
            return channel["tabs"]

    def __tab__(self, key, channelId=None, **kwargs):
        self.logger.info(f"__tab__(key={key}, channelId={channelId}, kwargs={kwargs})")
        if (channel := self.__channel__(channelId)):
            return (
                channel["channel"],
                self.__instance__.request(key, channelId, **kwargs)
            )

    @public
    def tab(self, key, **kwargs):
        self.logger.info(f"tab(key={key}, kwargs={kwargs})")
        return IVChannelVideos(*self.__tab__(key, **kwargs))

    @public
    def playlists(self, **kwargs):
        self.logger.info(f"playlists(kwargs={kwargs})")
        return IVChannelPlaylists(*self.__tab__("playlists", **kwargs))


    # playlist -----------------------------------------------------------------

    @public
    def playlist(self, playlistId=None, **kwargs):
        self.logger.info(f"playlist(playlistId={playlistId}, kwargs={kwargs})")
        if playlistId:
            return IVPlaylistVideos(
                self.__instance__.request("playlist", playlistId, **kwargs)
            )
        self.logger.error(f"Invalid playlistId: {playlistId}", notify=True)

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
