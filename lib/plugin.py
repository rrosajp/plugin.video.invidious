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
        self.__client__ = IVClient(self.logger)

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
        return self.playItem(*self.__client__.video(**kwargs))

    # channel ------------------------------------------------------------------

    # playlist -----------------------------------------------------------------

    # home ---------------------------------------------------------------------

    @action(category=30000)
    def home(self, **kwargs):
        if self.addDirectory(self.__client__.home()):
            return self.addSettingsItem()
        return False

    # feed ---------------------------------------------------------------------

    # popular ------------------------------------------------------------------

    @action(category=30200)
    def popular(self, **kwargs):
        if (items := self.__client__.popular(**kwargs)):
            return self.addDirectory(items, **kwargs)
        return False

    # trending -----------------------------------------------------------------

    # search -------------------------------------------------------------------

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
