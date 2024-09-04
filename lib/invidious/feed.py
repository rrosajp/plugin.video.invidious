# -*- coding: utf-8 -*-


from functools import wraps
from time import time

from iapc import public
from nuttig import containerRefresh, localizedString, notify, ICONINFO

from invidious.extract import IVChannel, IVVideo
from invidious.persistence import IVFeedChannels
from invidious.utils import confirm


# cached -----------------------------------------------------------------------

def cached(name):
    def decorator(func):
        @wraps(func)
        def wrapper(self, key, *args, **kwargs):
            cache = self.__cache__.setdefault(name, {})
            if ((value := cache.get(key)) is None):
                value = cache[key] = func(self, *(args or (key,)), **kwargs)
            return value
        return wrapper
    return decorator


# ------------------------------------------------------------------------------
# IVFeed

class IVFeed(object):

    def __init__(self, logger, instance, timeout=1800):
        self.logger = logger.getLogger(f"{logger.component}.feed")
        self.__instance__ = instance
        self.__cache__ = {}
        self.__channels__ = IVFeedChannels()
        self.__timeout__ = timeout
        self.__last__ = time()
        self.__keys__ = None
        self.__videos__ = []

    def __setup__(self):
        pass

    def __stop__(self):
        self.__cache__.clear()
        self.__instance__ = None
        self.logger.info("stopped")

    # --------------------------------------------------------------------------

    @cached("channels")
    def __channel__(self, channelId):
        self.logger.info(f"__channel__({channelId})")
        return IVChannel(self.__instance__.request("channel", channelId))

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

    def __update__(self, videos):
        self.__videos__ = sorted(
            videos, key=lambda x: x["published"], reverse=True
        )
        self.__last__ = time()

    def update(self, channels):
        videos = []
        cache = self.__cache__.setdefault("channels", {})
        for channel in channels:
            if channel:
                videos.extend(channel.pop("latestVideos", [])[:15])
                cache[channel["channelId"]] = (channel := IVChannel(channel))
        self.__update__(IVVideo(video) for video in videos)

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
        return [self.__channel__(key) for key in self.__channels__.keys()]

    @public
    def addChannel(self, key, value):
        self.__channels__.add(key)
        notify(localizedString(90002).format(value), icon=ICONINFO, time=1000)

    @public
    def removeChannel(self, key):
        self.__channels__.remove(key)
        containerRefresh()

    @public
    def clearChannels(self):
        if confirm():
            self.__channels__.clear()
            containerRefresh()
