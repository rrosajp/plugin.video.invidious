# -*- coding: utf-8 -*-


from time import time

from iapc import public
from iapc.tools import containerRefresh

from invidious.extract import IVChannel, IVVideo
from invidious.persistence import IVFeedChannels


# ------------------------------------------------------------------------------

def extractChannels(channels):
    return (IVChannel(channel) for channel in channels)

def extractVideos(videos):
    return (IVVideo(video) for video in videos)


# ------------------------------------------------------------------------------
# IVFeed

class IVFeed(object):

    def __init__(self, logger, instance, cache, timeout=1800):
        self.logger = logger.getLogger(f"{logger.component}.feed")
        self.__instance__ = instance
        self.__cache__ = cache.setdefault("channels", {})
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

    def __update_cache__(self, channel):
        # this is wonky, but I couldn't bring myself to move
        # the channel cache from the service to the feed.
        # ¯\_(ツ)_/¯
        self.__cache__[channel["channelId"]] = channel

    def __update_videos__(self, videos):
        self.__videos__ = sorted(
            videos, key=lambda x: x["published"], reverse=True
        )
        self.__last__ = time()

    def update(self, channels):
        _videos_ = []
        for channel in channels:
            _videos_.extend(channel.pop("latestVideos", [])[:15])
            self.__update_cache__(IVChannel(channel)) # see __update_cache__
        self.__update_videos__(IVVideo(video) for video in _videos_)

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
            self.update(self.__instance__.map_request("channel", keys))
        return self.page(limit, page)

    # channels -----------------------------------------------------------------

    @public
    def channels(self):
        self.logger.info(f"channels()")
        return [self.__cache__[key] for key in self.__channels__.keys()]
        #return []

    @public
    def addChannel(self, key):
        self.__channels__.add(key)

    @public
    def removeChannel(self, key):
        self.__channels__.remove(key)
        containerRefresh()

    @public
    def clearChannels(self):
        self.__channels__.clear()
        containerRefresh()
