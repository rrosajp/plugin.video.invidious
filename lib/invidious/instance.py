# -*- coding: utf-8 -*-


from functools import wraps

from requests import HTTPError

from iapc import public
from nuttig import (
    buildUrl, getSetting, localizedString, selectDialog, setSetting
)

from invidious.extract import IVVideo, IVVideos
from invidious.regional import regions
from invidious.session import IVSession
from invidious.ytdlp import YtDlp


# cached -----------------------------------------------------------------------

def cached(name):
    def decorator(func):
        @wraps(func)
        def wrapper(self, key, *args, **kwargs):
            cache = self.__cache__.setdefault(name, {})
            if (
                (not (value := cache.get(key))) or
                (
                    (expires := getattr(value, "__expires__", None)) and
                    (time() >= expires)
                )
            ):
                value = cache[key] = func(self, *(args or (key,)), **kwargs)
            return value
        return wrapper
    return decorator


# ------------------------------------------------------------------------------
# IVInstance

class IVInstance(object):

    __headers__ = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "*",
        "Accept-Encoding": "gzip, deflate, br, zstd"
    }

    def __init__(self, logger):
        self.logger = logger.getLogger(f"{logger.component}.instance")
        self.__session__ = IVSession(self.logger, headers=self.__headers__)
        self.__ytdlp__ = YtDlp(self.logger)
        self.__cache__ = {}

    def __setup__(self):
        if (uri := getSetting("instance.uri", str)):
            self.__url__ = buildUrl(uri, getSetting("instance.path", str))
        else:
            self.__url__ = None
        self.logger.info(f"Url: {self.__url__}")

        self.__locale__ = "en-US"
        #getSetting("regional.locale", str)
        #self.logger.info(
        #    f"{localizedString(41221)}: "
        #    f"({self.__locale__})\\t{getSetting('regional.locale.text', str)}"

        self.__region__ = getSetting("regional.region", str)
        self.logger.info(
            f"{localizedString(41211)}: "
            f"({self.__region__})\\t{getSetting('regional.region.text', str)}"
        )

        self.__session__.__setup__()
        self.__ytdlp__.__setup__()
        self.__cache__.clear()

    def __stop__(self):
        self.__cache__.clear()
        self.__ytdlp__.__stop__()
        self.__session__.__stop__()
        self.logger.info("stopped")

    # instance -----------------------------------------------------------------

    def __instances__(self):
        return self.__session__.__get__(
            "https://api.invidious.io/instances.json", sort_by="location"
        )

    def instances(self):
        return {
            instance["uri"]: f"({instance['region']})\t{name}"
            for name, instance in self.__instances__()
            if (instance["api"] and (instance["type"] in ("http", "https")))
        }

    @public
    def instance(self):
        return self.__url__

    @public
    def selectInstance(self):
        if (instances := self.instances()):
            uri = getSetting("instance.uri", str)
            keys = list(instances.keys())
            values = list(instances.values())
            preselect = keys.index(uri) if uri in keys else -1
            index = selectDialog(values, heading=41113, preselect=preselect)
            if index > -1:
                setSetting("instance.uri", keys[index], str)
                return True
        return False

    # region -------------------------------------------------------------------

    @public
    def selectRegion(self):
        region = getSetting("regional.region", str)
        keys = list(regions.keys())
        values = list(regions.values())
        preselect = keys.index(region) if region in regions else -1
        if (
            (
                index := selectDialog(
                    [f"({k})\t{v}" for k, v in regions.items()],
                    heading=41212,
                    preselect=preselect
                )
            ) > -1
        ):
            setSetting("regional.region", keys[index], str)
            setSetting("regional.region.text", values[index], str)

    # --------------------------------------------------------------------------

    def __regional__(self, regional, kwargs):
        if regional:
            kwargs["region"] = self.__region__
        elif "region" in kwargs:
            del kwargs["region"]
        kwargs["hl"] = self.__locale__

    __paths__ = {
        "video": "videos/{}",
        "channel": "channels/{}",
        "playlist": "playlists/{}",
        "videos": "channels/{}/videos",
        "playlists": "channels/{}/playlists",
        "streams": "channels/{}/streams",
        "shorts": "channels/{}/shorts"
    }

    def __buildUrl__(self, key, *arg):# *arg is a trick
        return buildUrl(self.__url__, self.__paths__.get(key, key).format(*arg))

    def __get__(self, key, *arg, regional=True, **kwargs):# *arg is a trick
        if self.__url__:
            self.__regional__(regional, kwargs)
            return self.__session__.__get__(
                self.__buildUrl__(key, *arg), **kwargs
            )

    def __map_get__(self, key, args, regional=True, **kwargs):
        if self.__url__:
            self.__regional__(regional, kwargs)
            return self.__session__.__map_get__(
                (self.__buildUrl__(key, arg) for arg in args), **kwargs
            )

    # cached -------------------------------------------------------------------

    @cached("videos")
    def __video__(self, videoId):
        return IVVideo(self.__get__("video", videoId))

    # video --------------------------------------------------------------------

    @public
    def video(self, **kwargs):
        if (videoId := kwargs.pop("videoId", None)):
            if kwargs:
                return self.__ytdlp__.video(videoId, **kwargs)
            return self.__video__(videoId)
        self.logger.error(f"Invalid videoId: {videoId}", notify=True)

    # popular ------------------------------------------------------------------

    @public
    def popular(self, **kwargs):
        if (videos := self.__get__("popular", regional=False, **kwargs)):
            return IVVideos(videos)
