# -*- coding: utf-8 -*-


from iapc import public, Service
from iapc.tools import (
    containerRefresh, getSetting, makeProfile, notify, ICONERROR
)

from invidious.extract import extractItems, Video
from invidious.folders import home
from invidious.search import IVSearch
from invidious.session import IVSession


# ------------------------------------------------------------------------------
# IVService

class IVService(Service):

    def __init__(self, *args, **kwargs):
        super(IVService, self).__init__(*args, **kwargs)
        makeProfile()
        self.__session__ = IVSession(self.logger, "service.session")
        self.__search__ = IVSearch(self.logger, "service.search")
        self.__home__ = home

    def __setup__(self):
        self.__session__.__setup__()
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

    # --------------------------------------------------------------------------
    # public api
    # --------------------------------------------------------------------------

    # instance -----------------------------------------------------------------

    @public
    def instances(self, **kwargs):
        return {
            instance["uri"]: f"({instance['region']})\t{name}"
            for name, instance in self.__session__.instances(**kwargs)
            if (instance["api"] and (instance["type"] in ("http", "https")))
        }

    @public
    def instance(self):
        return self.__session__.__instance__

    # play ---------------------------------------------------------------------

    @public
    def play(self, **kwargs):
        self.logger.info(f"play(kwargs={kwargs})")
        if (videoId := kwargs.pop("videoId")):
            if (video := Video(self.__session__.query("video", videoId))):
                return (video, "mpd", {"mimeType": "application/dash+xml"})
        self.__raise__("Missing videoId", throw=False)
        return (None, "", {})

    # home ---------------------------------------------------------------------

    @public
    def home(self):
        return self.__home__

    # search -------------------------------------------------------------------

    @public
    def search(self, **kwargs):
        self.logger.info(f"search(kwargs={kwargs})")
        if (kwargs := self.__search__.search(**kwargs)):
            return extractItems(self.__session__.query("search", **kwargs))



# __main__ ---------------------------------------------------------------------

if __name__ == "__main__":
    IVService().start()
