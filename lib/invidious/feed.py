# -*- coding: utf-8 -*-


from itertools import chain
from time import time

from iapc import public
from iapc.tools import containerRefresh

from invidious.extract import IVVideo
from invidious.persistence import IVFeedChannels


# ------------------------------------------------------------------------------
# IVFeed

class IVFeed(object):

    def __init__(self, logger, instance, timeout=1800):
        self.logger = logger.getLogger(f"{logger.component}.feed")
        self.__instance__ = instance
        self.__channels__ = IVFeedChannels()
        self.__timeout__ = timeout
        self.__last__ = time()
        self.__keys__ = None
        self.__videos__ = []

    def __setup__(self):
        pass

    def __stop__(self):
        self.__instance__ = None
        self.logger.info("stopped")

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

    def update(self, videos):
        self.__videos__ = sorted(
            (IVVideo(video) for video in videos),
            key=lambda x: x["published"], reverse=True
        )
        self.__last__ = time()

    def page(self, limit, page):
        return self.__videos__[(limit * (page - 1)):(limit * page)]

    # feed ---------------------------------------------------------------------

    @public
    def feed(self, limit, page=1):
        self.logger.info(f"feed(limit={limit}, page={page})")
        if (
            ((page := int(page)) == 1) and
            ((keys := self.invalid()) is not None)
        ):
            channels = self.__instance__.map_request("channel", keys)
            self.update(
                chain.from_iterable(
                    channel["latestVideos"][:15] for channel in channels
                )
            )
        return self.page(limit, page)

    # public methods -----------------------------------------------------------

    @public
    def addChannel(self, key):
        self.__channels__.add(key)

    @public
    def removeChannel(self, key):
        self.__channels__.remove(key)

    @public
    def clearChannels(self):
        self.__channels__.clear()
