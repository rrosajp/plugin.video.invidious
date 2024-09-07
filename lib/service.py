# -*- coding: utf-8 -*-


from iapc import public, Service
from nuttig import containerRefresh, getSetting, makeProfile

from invidious.extract import (
    extractIVVideos, IVChannel, IVChannelPlaylists,
    IVChannelVideos, IVPlaylistVideos, IVVideo
)
from invidious.feed import IVFeed
from invidious.folders import home, subFolders
from invidious.instance import IVInstance
from invidious.search import IVSearch
from invidious.ytdlp import YtDlp


# ------------------------------------------------------------------------------
# IVService

class IVService(Service):

    def __init__(self, *args, **kwargs):
        super(IVService, self).__init__(*args, **kwargs)
        makeProfile()
        self.__instance__ = IVInstance(self.logger)
        self.__search__ = IVSearch(self.logger, self.__instance__)
        self.__feed__ = IVFeed(self.logger, self.__instance__)
        self.__ytdlp__ = YtDlp(self.logger)

    def __setup__(self):
        self.__instance__.__setup__()
        self.__search__.__setup__()
        self.__feed__.__setup__()
        self.__ytdlp__.__setup__()

    def __stop__(self):
        self.__ytdlp__.__stop__()
        self.__feed__.__stop__()
        self.__search__.__stop__()
        self.__instance__.__stop__()
        self.logger.info("stopped")

    def start(self, **kwargs):
        self.logger.info("starting...")
        self.__setup__()
        self.serve(**kwargs)
        self.__stop__()

    def onSettingsChanged(self):
        self.__setup__()
        containerRefresh()

    # play ---------------------------------------------------------------------

    @public
    def play(self, videoId=None, yt=False, iv=False):
        self.logger.info(f"play(videoId={videoId}, ytdlp={ytdlp})")
        if videoId:
            video = IVVideo(self.__instance__.request("video", videoId))
            if video and (yt or iv):
                if (not (info := self.__ytdlp__.play(videoId, yt=yt, iv=iv))):
                    return None
                video["url"] = info["url"]
                video["manifestType"] = info["manifestType"]
            return video
        self.logger.error(f"Invalid videoId: {videoId}", notify=True)

    # channel ------------------------------------------------------------------

    def __channel__(self, channelId):
        self.logger.info(f"__channel__({channelId})")
        if channelId:
            return self.__feed__.__channel__(channelId)
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
                self.__instance__.request(
                    "playlist", playlistId, regional=False, **kwargs
                )
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

    # popular ------------------------------------------------------------------

    @public
    def popular(self, **kwargs):
        self.logger.info(f"popular(kwargs={kwargs})")
        return extractIVVideos(
            self.__instance__.request("popular", regional=False, **kwargs)
        )

    # trending -----------------------------------------------------------------

    @public
    def trending(self, folders=False, **kwargs):
        self.logger.info(f"trending(kwargs={kwargs})")
        if folders:
            return subFolders.get("trending", [])
        return extractIVVideos(self.__instance__.request("trending", **kwargs))


# __main__ ---------------------------------------------------------------------

if __name__ == "__main__":
    service = IVService()
    kwargs = {
        "instance": service.__instance__,
        "search": service.__search__,
        "feed": service.__feed__
    }
    service.start(**kwargs)
