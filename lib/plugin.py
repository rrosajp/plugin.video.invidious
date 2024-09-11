# -*- coding: utf-8 -*-


from time import time

from sys import argv
from urllib.parse import urlencode

from inputstreamhelper import Helper

from nuttig import action, getSetting, openSettings, parseQuery, Plugin

from invidious.client import IVClient
from invidious.utils import channelsItem, moreItem, newQueryItem, settingsItem


# ------------------------------------------------------------------------------
# IVPlugin

class IVPlugin(Plugin):

    def __init__(self, *args, **kwargs):
        super(IVPlugin, self).__init__(*args, **kwargs)
        self.__client__ = IVClient()

    # helpers ------------------------------------------------------------------

    def addMore(self, more, count=0, **kwargs):
        if more is True:
            if (index := kwargs.get("index")):
                if count:
                    kwargs["index"] = int(index) + count
                else:
                    del kwargs["index"]
            else:
                kwargs["page"] = int(kwargs.get("page", 1)) + 1
        else:
            kwargs["continuation"] = more
        return self.addItem(
            moreItem(self.url, action=self.action, **kwargs)
        )

    def addDirectory(self, items, *args, **kwargs):
        if super(IVPlugin, self).addDirectory(items, *args):
            if (more := getattr(items, "more", None)):
                return self.addMore(more, count=len(items), **kwargs)
            return True
        return False

    def addSettingsItem(self):
        if getSetting("home.settings", bool):
            return self.addItem(settingsItem(self.url, action="settings"))
        return True

    def addNewQueryItem(self):
        return self.addItem(newQueryItem(self.url, action="search", new=True))

    def addChannelsItem(self):
        return self.addItem(channelsItem(self.url, action="channels"))

    def playItem(
        self, item, manifestType, mimeType=None, headers=None, params=None
    ):
        if item:
            if not Helper(manifestType).check_inputstream():
                return False
            item.setProperty("inputstream", "inputstream.adaptive")
            item.setProperty("inputstream.adaptive.manifest_type", manifestType)
            if headers and isinstance(headers, dict):
                item.setProperty(
                    "inputstream.adaptive.manifest_headers", urlencode(headers)
                )
            if params and isinstance(params, dict):
                item.setProperty(
                    "inputstream.adaptive.manifest_params", urlencode(params)
                )
            return super(IVPlugin, self).playItem(item, mimeType=mimeType)
        return False

    # play ---------------------------------------------------------------------

    @action()
    def play(self, **kwargs):
        return self.playItem(*self.__client__.play(**kwargs))

    # channel ------------------------------------------------------------------

    @action()
    def channel(self, **kwargs):
        if (
            (not ("continuation" in kwargs)) and
            (tabs := self.__client__.tabs(**kwargs)) and
            (not self.addItems(tabs))
        ):
            return False
        return self.addDirectory(
            self.__client__.tab("videos", **kwargs), **kwargs
        )

    @action(category=30203)
    def playlists(self, **kwargs):
        return self.addDirectory(self.__client__.playlists(**kwargs), **kwargs)

    @action(category=30204)
    def streams(self, **kwargs):
        return self.addDirectory(
            self.__client__.tab("streams", **kwargs), **kwargs
        )

    @action(category=30205)
    def shorts(self, **kwargs):
        return self.addDirectory(
            self.__client__.tab("shorts", **kwargs), **kwargs
        )

    # playlist -----------------------------------------------------------------

    @action()
    def playlist(self, index=50, **kwargs):
        return self.addDirectory(
            self.__client__.playlist(index=index, **kwargs),
            index=index,
            **kwargs
        )

    # home ---------------------------------------------------------------------

    @action(category=30000)
    def home(self, **kwargs):
        if self.addDirectory(self.__client__.home()):
            return self.addSettingsItem()
        return False

    # feed ---------------------------------------------------------------------

    @action(category=30101, cacheToDisc=False)
    def feed(self, **kwargs):
        t = time()
        try:
            if ((int(kwargs.get("page", 1)) == 1) and (not self.addChannelsItem())):
                return False
            return self.addDirectory(self.__client__.feed(**kwargs), **kwargs)
        finally:
            self.logger.info(f"feed() took: {time() - t} seconds")

    @action(category=30206)
    def channels(self, **kwargs):
        return self.addDirectory(self.__client__.channels(), **kwargs)

    # explore ------------------------------------------------------------------

    #@action(category=30106)
    #def explore(self, **kwargs):
    #    return self.addDirectory(self.__client__.explore(), **kwargs)

    # popular ------------------------------------------------------------------

    @action(category=30104)
    def popular(self, **kwargs):
        return self.addDirectory(self.__client__.popular(**kwargs), **kwargs)

    # trending -----------------------------------------------------------------

    @action(category=30105)
    def trending(self, **kwargs):
        if (
            (not "type" in kwargs) and
            not self.addItems(self.__client__.trending(folders=True))
        ):
            return False
        return self.addDirectory(self.__client__.trending(**kwargs), **kwargs)

    # search -------------------------------------------------------------------

    def __query__(self):
        return self.__client__.query()

    def __history__(self):
        if self.addNewQueryItem():
            return self.addDirectory(self.__client__.history())
        return False

    def __search__(self, query):
        return self.addDirectory(self.__client__.search(query), **query)

    @action(category=30102)
    def search(self, **kwargs):
        if kwargs:
            if (query := (self.__query__() if "new" in kwargs else kwargs)):
                return self.__search__(query)
            return False
        return self.__history__()

    # settings -----------------------------------------------------------------

    @action(directory=False)
    def settings(self, **kwargs):
        openSettings()
        return True


# __main__ ---------------------------------------------------------------------

def dispatch(url, handle, query, *args):
    IVPlugin(url, int(handle)).dispatch(**parseQuery(query))


if __name__ == "__main__":
    dispatch(*argv)
