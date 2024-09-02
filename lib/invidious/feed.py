# -*- coding: utf-8 -*-


from time import time

from iapc import public

from invidious.persistence import IVFeedChannels


# ------------------------------------------------------------------------------
# IVFeed

class IVFeed(object):

    def __init__(self, logger, timeout=1800):
        self.logger = logger.getLogger(f"{logger.component}.feed")
        self.__channels__ = IVFeedChannels()
        self.__timeout__ = timeout
        self.__last__ = time()
        self.__keys__ = None
        self.__contents__ = []

    def __setup__(self):
        pass

    def __stop__(self):
        pass

    # --------------------------------------------------------------------------

    def __invalid__(self, keys):
        return (self.__keys__ != keys)

    def __expired__(self):
        return ((time() - self.__last__) > self.__timeout__)

    def invalid(self):
        if (invalid := self.__invalid__(keys := set(self.__channels__.keys()))):
            self.__keys__ = keys
        if (invalid or self.__expired__()):
            return self.__keys__

    def update(self, feeds):
        self.__contents__ = sorted(
            feeds, key=lambda x: x["published"], reverse=True
        )
        self.__last__ = time()

    def page(self, limit, page):
        return {
            "contents": self.__contents__[(limit * (page - 1)):(limit * page)],
            "continuation": None
        }

    # public methods -----------------------------------------------------------

    @public
    def addChannel(self, key):
        self.__channels__.add(key)

    @public
    def removeChannel(self, key):
        self.__channels__.remove(key)
