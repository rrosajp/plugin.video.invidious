# -*- coding: utf-8 -*-


from concurrent.futures import ThreadPoolExecutor

from iapc.tools import (
    buildUrl, getSetting, localizedString, selectDialog, setSetting
)

from invidious.session import IVSession


# ------------------------------------------------------------------------------
# IVInstance

class IVInstance(object):

    headers = {}

    def __init__(self, logger):
        self.logger = logger.getLogger(f"{logger.component}.instance")
        self.session = IVSession(self.logger, headers=self.headers)

    def __setup__(self):
        if (uri := getSetting("instance.uri", str)):
            self.instance = buildUrl(uri, getSetting("instance.path", str))
        else:
            self.instance = None
        self.logger.info(f"{localizedString(40110)}: {self.instance}")

        if (timeout := getSetting("instance.timeout", float)) > 0.0:
            self.timeout = (((timeout - (timeout % 3)) + 0.05), timeout)
        else:
            self.timeout = None
        self.logger.info(f"{localizedString(40116)}: {self.timeout}")
        self.region = getSetting("regional.region", str)
        self.logger.info(
            f"{localizedString(40124)}: "
            f"{self.region} - {getSetting('regional.region.text', str)}"
        )

    def __get__(self, *args, **kwargs):
        return self.session.get(*args, params=kwargs, timeout=self.timeout)

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

    # get ----------------------------------------------------------------------

    def get(self, path, regional=True, **kwargs):
        if self.instance:
            self.logger.info(f"get(url={buildUrl(self.instance, path)})")
            self.logger.info(f"get(kwargs={kwargs})")
            if regional:
                kwargs["region"] = self.region
            else:
                kwargs.pop("region", None)
            return self.__get__(buildUrl(self.instance, path), **kwargs)

    # query --------------------------------------------------------------------

    __paths__ = {
        "video": "videos/{}",
        "channel": "channels/{}",
        "playlist": "playlists/{}",
        "videos": "channels/{}/videos",
        "playlists": "channels/{}/playlists"
    }

    def query(self, key, *args, **kwargs):
        return self.get(self.__paths__.get(key, key).format(*args), **kwargs)
