# -*- coding: utf-8 -*-


from iapc import public, Service
from iapc.tools import containerRefresh, getSetting, localizedString, makeProfile

from invidious.session import InvidiousSession


# ------------------------------------------------------------------------------
# InvidiousService

class InvidiousService(Service):

    def __init__(self, *args, **kwargs):
        super(InvidiousService, self).__init__(*args, **kwargs)
        self.__session__ = InvidiousSession(self.logger, "service.session")
        makeProfile()

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

    @public
    def home(self):
        return []

# __main__ ---------------------------------------------------------------------

if __name__ == "__main__":
    InvidiousService().start()
