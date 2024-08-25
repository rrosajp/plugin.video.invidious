# -*- coding: utf-8 -*-


from iapc import public, Service
from iapc.tools import (
    containerRefresh, getSetting, makeProfile, notify, ICONERROR
)

from invidious.extract import extractIVItems, IVVideo
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
        self.__search__ = IVSearch(self.logger)

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

    # instance -----------------------------------------------------------------

    @public
    def instance(self):
        return self.__instance__.instance

    @public
    def selectInstance(self):
        return self.__instance__.selectInstance()

    # play ---------------------------------------------------------------------

    @public
    def play(self, **kwargs):
        self.logger.info(f"play(kwargs={kwargs})")
        if (videoId := kwargs.pop("videoId")):
            return IVVideo(self.__instance__.query("video", videoId))
        self.__raise__("Missing videoId", throw=False)

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

    # search -------------------------------------------------------------------

    @public
    def search(self, **kwargs):
        self.logger.info(f"search(kwargs={kwargs})")
        if (kwargs := self.__search__.search(**kwargs)):
            return extractIVItems(self.__instance__.query("search", **kwargs))


# __main__ ---------------------------------------------------------------------

if __name__ == "__main__":
    IVService().start()
