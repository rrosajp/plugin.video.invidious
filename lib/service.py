# -*- coding: utf-8 -*-


from iapc import public, Service
from iapc.tools import containerRefresh, getSetting, makeProfile

from invidious.folders import home, subFolders
from invidious.session import InvidiousSession


# ------------------------------------------------------------------------------
# InvidiousService

class InvidiousService(Service):

    def __init__(self, *args, **kwargs):
        super(InvidiousService, self).__init__(*args, **kwargs)
        makeProfile()
        self.__session__ = InvidiousSession(self.logger, "service.session")
        self.__home__ = home
        self.__subFolders__ = subFolders
        self.__query__ = {}

    def __setup__(self):
        self.__session__.__setup__()

    def start(self, **kwargs):
        self.logger.info("starting...")
        self.__setup__()
        self.serve(**kwargs)
        self.logger.info("stopped")

    def onSettingsChanged(self):
        self.__setup__()
        containerRefresh()

    # public api ---------------------------------------------------------------

    @public
    def instances(self, **kwargs):
        return {
            instance["uri"]: f"[{instance['region']}]\t{name}"
            for name, instance in self.__session__.instances(**kwargs)
            if (instance["api"] and (instance["type"] in ("http", "https")))
        }

    @public
    def instance(self):
        return self.__session__.__instance__

    # --------------------------------------------------------------------------

    @public
    def home(self):
        return self.__home__

    @public
    def subFolders(self):
        return self.__subFolders__

    @public
    def pushQuery(self, query):
        self.__query__ = query

# __main__ ---------------------------------------------------------------------

if __name__ == "__main__":
    InvidiousService().start()
