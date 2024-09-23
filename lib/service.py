# -*- coding: utf-8 -*-


from iapc import public, Service
from nuttig import containerRefresh, getSetting, makeProfile

from invidious.feed import IVFeed
from invidious.folders import getFolders
from invidious.instance import IVInstance
from invidious.search import IVSearch


# ------------------------------------------------------------------------------
# IVService

class IVService(Service):

    def __init__(self, *args, **kwargs):
        super(IVService, self).__init__(*args, **kwargs)
        makeProfile()
        self.__folders__ = {}
        self.__instance__ = IVInstance(self.logger)

    def __setup__(self):
        self.__instance__.__setup__()

    def __stop__(self):
        self.__instance__.__stop__()
        self.__folders__.clear()
        self.logger.info("stopped")

    def start(self, **kwargs):
        self.logger.info("starting...")
        self.__setup__()
        self.serve(**kwargs)
        self.__stop__()

    def onSettingsChanged(self):
        self.__setup__()
        containerRefresh()

    # video --------------------------------------------------------------------

    @public
    def video(self, **kwargs):
        if (videoId := kwargs.pop("videoId")):
            return self.__instance__.video(videoId, **kwargs)
        self.logger.error(f"Invalid videoId: {videoId}", notify=True)

    # channel ------------------------------------------------------------------

    # playlist -----------------------------------------------------------------

    # folders ------------------------------------------------------------------

    @public
    def folders(self, *paths):
        folders = self.__folders__.setdefault(paths, getFolders(*paths))
        return [
            folder for folder in folders
            if (not (setting := folder["setting"])) or getSetting(setting, bool)
        ]

    # popular ------------------------------------------------------------------

    # trending -----------------------------------------------------------------


# __main__ ---------------------------------------------------------------------

if __name__ == "__main__":
    (service := IVService()).start(
        instance=service.__instance__,
        #search=service.__search__,
        #feed=service.__feed__
    )
