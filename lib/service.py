# -*- coding: utf-8 -*-


from iapc import public, Service
from iapc.tools import (
    containerRefresh, getSetting, makeProfile, notify, ICONERROR
)

from invidious.extract import IVVideo, IVPlaylistVideos
from invidious.folders import home
from invidious.instance import IVInstance
from invidious.search import IVSearch


# ------------------------------------------------------------------------------
# IVService

class IVService(Service):

    def __init__(self, *args, **kwargs):
        super(IVService, self).__init__(*args, **kwargs)
        makeProfile()
        self.__instance__ = IVInstance(self.logger)
        self.__search__ = IVSearch(self.logger, self.__instance__)

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

    # playlist -----------------------------------------------------------------

    def __playlist__(self, playlistId):
        self.logger.info(f"__playlist__({playlistId})")
        #page = 1
        #result = []
        #while (
        #    videos := (
        #        playlist := self.__instance__.request(
        #            "playlist", playlistId, page=page
        #        )
        #    )["videos"]
        #):
        #    page += 1
        #    result.extend(videos)
        index = 50
        result = []
        playlist = self.__instance__.request("playlist", playlistId, index=index)
        videoCount = playlist["videoCount"]
        videos = playlist["videos"]
        result.extend(videos)
        while len(result) < videoCount:
            #index += len(videos)
            #playlist = self.__instance__.request("playlist", playlistId, index=index)
            #videos = playlist["videos"]
            index += len(videos)
            videos = self.__instance__.request("playlist", playlistId, index=index)["videos"]
            result.extend(videos)

        self.logger.info(f"len(result): {len(result)}")

    @public
    def playlist(self, **kwargs):
        self.logger.info(f"playlist(kwargs={kwargs})")
        if (playlistId := kwargs.pop("playlistId")):

            #self.__playlist__(playlistId)

            return IVPlaylistVideos(
                self.__instance__.request("playlist", playlistId, **kwargs)
            )
            #playlist = self.__instance__.request(
            #    "playlist", playlistId, **kwargs
            #)
            #return (
            #    playlist["title"],
            #    [IVVideo(video) for video in playlist["videos"]]
            #)
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
