# -*- coding: utf-8 -*-


from iapc import public
from nuttig import (
    buildUrl, getSetting, localizedString, selectDialog, setSetting
)

from invidious.regional import regions
from invidious.session import IVSession


# ------------------------------------------------------------------------------
# IVInstance

class IVInstance(object):

    headers = {}

    def __init__(self, logger):
        self.logger = logger.getLogger(f"{logger.component}.instance")
        self.__session__ = IVSession(self.logger, headers=self.headers)

    def __setup__(self):
        if (uri := getSetting("instance.uri", str)):
            self.__instance__ = buildUrl(uri, getSetting("instance.path", str))
        else:
            self.__instance__ = None
        self.logger.info(f"{localizedString(40110)}: {self.__instance__}")

        if (timeout := getSetting("instance.timeout", float)) > 0.0:
            self.__timeout__ = (((timeout - (timeout % 3)) + 0.05), timeout)
        else:
            self.__timeout__ = None
        self.logger.info(f"{localizedString(40116)}: {self.__timeout__}")
        self.region = getSetting("regional.region", str)
        self.logger.info(
            f"{localizedString(40124)}: "
            f"{self.region} - {getSetting('regional.region.text', str)}"
        )

    def __stop__(self):
        self.__session__.close()
        self.logger.info("stopped")

    def __get__(self, url, **kwargs):
        return self.__session__.get(
            url, params=kwargs, timeout=self.__timeout__
        )

    def __map_get__(self, urls, **kwargs):
        return self.__session__.map_get(
            urls, params=kwargs, timeout=self.__timeout__
        )

    # instance -----------------------------------------------------------------

    def __instances__(self):
        return self.__get__(
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
        return self.__instance__

    @public
    def selectInstance(self):
        if (instances := self.instances()):
            uri = getSetting("instance.uri", str)
            keys = list(instances.keys())
            values = list(instances.values())
            preselect = keys.index(uri) if uri in keys else -1
            index = selectDialog(values, heading=40113, preselect=preselect)
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
                    heading=40123,
                    preselect=preselect
                )
            ) > -1
        ):
            setSetting("regional.region", keys[index], str)
            setSetting("regional.region.text", values[index], str)

    # get ----------------------------------------------------------------------

    def __region__(self, regional, kwargs):
        if regional:
            kwargs["region"] = self.region
        else:
            kwargs.pop("region", None)

    def get(self, path, regional=True, **kwargs):
        if self.__instance__:
            self.__region__(regional, kwargs)
            return self.__get__(buildUrl(self.__instance__, path), **kwargs)

    def map_get(self, paths, regional=True, **kwargs):
        if self.__instance__:
            self.__region__(regional, kwargs)
            return self.__map_get__(
                (buildUrl(self.__instance__, path) for path in paths), **kwargs
            )

    # query --------------------------------------------------------------------

    __paths__ = {
        "video": "videos/{}",
        "channel": "channels/{}",
        "playlist": "playlists/{}",
        "videos": "channels/{}/videos",
        "playlists": "channels/{}/playlists",
        "streams": "channels/{}/streams",
        "shorts": "channels/{}/shorts"
    }

    def request(self, key, *args, **kwargs):
        return self.get(self.__paths__.get(key, key).format(*args), **kwargs)

    def map_request(self, key, args, **kwargs):
        #path = self.__paths__.get(key, key)
        return self.map_get(
            (self.__paths__.get(key, key).format(arg) for arg in args), **kwargs
        )
