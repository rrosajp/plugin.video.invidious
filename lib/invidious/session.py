# -*- coding: utf-8 -*-


from requests import Session, Timeout

from iapc.tools import buildUrl, getSetting, localizedString, notify, ICONERROR


# ------------------------------------------------------------------------------
# BaseSession

class BaseSession(Session):

    def __init__(self, logger, name, headers=None):
        super(BaseSession, self).__init__()
        self.logger = logger.getLogger(name)
        if headers:
            self.headers.update(headers)

    def __setup__(self):
        if (timeout := getSetting("instance.timeout", float)) <= 0.0:
            self.__timeout__ = None
        else:
            self.__timeout__ = (((timeout - (timeout % 3)) + 0.05), timeout)
        self.logger.info(f"{localizedString(40116)}: {self.__timeout__}")

    def request(self, method, url, **kwargs):
        self.logger.info(
            f"request: {method} {buildUrl(url, **kwargs.get('params', {}))}"
        )
        try:
            response = super(BaseSession, self).request(
                method, url, timeout=self.__timeout__, **kwargs
            )
        except Timeout as error:
            self.logger.error(message := f"error: {error}")
            notify(message, icon=ICONERROR)
        else:
            response.raise_for_status()
            return response


# ------------------------------------------------------------------------------
# InvidiousSession

class InvidiousSession(BaseSession):

    __headers__ = {
    }

    def __init__(self, logger, name):
        super(InvidiousSession, self).__init__(
            logger, name, headers=self.__headers__
        )

    def __setup__(self):
        self.__url__ = buildUrl(
            getSetting("instance.uri", str), getSetting("instance.path", str)
        )
        self.logger.info(f"{localizedString(40110)}: {self.__url__}")
        super(InvidiousSession, self).__setup__()
        self.__region__ = getSetting("regional.region", str)
        self.logger.info(
            f"{localizedString(40124)}: {getSetting('regional.region.text', str)}"
        )

    def request(self, *args, **kwargs):
        return super(InvidiousSession, self).request(*args, **kwargs).json()

    def __get__(self, *args, **kwargs):
        return super(InvidiousSession, self).get(*args, params=kwargs)

    def get(self, path, regional=True, **kwargs):
        self.logger.info(f"url: {buildUrl(self.__url__, url)}")
        #if regional:
        #    kwargs["region"] = self.__region__
        #else:
        #    kwargs.pop("region", None)
        #return self.__get__(buildUrl(self.__url__, url), **kwargs)

    # --------------------------------------------------------------------------

    __paths__ = {
        "video": "videos/{}",
        "channel": "channels/{}",
        "playlist": "playlists/{}",
        "videos": "channels/{}/videos",
        "playlists": "channels/{}/playlists"
    }

    def query(self, key, *args, **kwargs):
        return self.get(self.__paths__.get(key, key).format(*args), **kwargs)

    # --------------------------------------------------------------------------

    __instances__ = "https://api.invidious.io/instances.json"

    def instances(self, **kwargs):
        return self.__get__(self.__instances__, **kwargs)

    # --------------------------------------------------------------------------

    def channel(self, channelId):
        if (channel := self.query("channel", channelId)):
            self.logger.info(f"channel: {channel}")
