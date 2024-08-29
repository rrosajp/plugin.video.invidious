# -*- coding: utf-8 -*-


from sys import argv
from urllib.parse import urlencode

from inputstreamhelper import Helper

from iapc.tools import action, executeBuiltin, getSetting, openSettings, parseQuery, Plugin

from invidious.client import IVClient
from invidious.utils import moreItem, newQueryItem, settingsItem


# ------------------------------------------------------------------------------
# IVPlugin

class IVPlugin(Plugin):

    def __init__(self, *args, **kwargs):
        super(IVPlugin, self).__init__(*args, **kwargs)
        self.__client__ = IVClient()

    # helpers ------------------------------------------------------------------

    def addMore(self, more, **kwargs):
        if more is True:
            kwargs["page"] = int(kwargs.get("page", 1)) + 1
        else:
            kwargs["continuation"] = more
        return self.addItem(
            moreItem(self.url, action=self.action, **kwargs)
        )

    def addDirectory(self, items, *args, **kwargs):
        if super(IVPlugin, self).addDirectory(items, *args):
            if (more := getattr(items, "more", None)):
                return self.addMore(more, **kwargs)
            return True
        return False

    def addSettingsItem(self):
        if getSetting("home.settings", bool):
            return self.addItem(settingsItem(self.url, action="settings"))
        return True

    def addNewQueryItem(self):
        return self.addItem(newQueryItem(self.url, action="search", new=True))

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
        self.logger.info(f"play(kwargs={kwargs})")
        return self.playItem(*self.__client__.play(**kwargs))

    # channel ------------------------------------------------------------------

    @action()
    def channel(self, **kwargs):
        self.logger.info(f"channel(kwargs={kwargs})")
        return True

    # playlist -----------------------------------------------------------------

    @action()
    def playlist(self, **kwargs):
        self.logger.info(f"playlist(kwargs={kwargs})")
        return self.addDirectory(self.__client__.playlist(**kwargs), **kwargs)

    # home ---------------------------------------------------------------------

    @action(category=30000)
    def home(self, **kwargs):
        if self.addDirectory(self.__client__.home()):
            return self.addSettingsItem()
        return False

    # feed ---------------------------------------------------------------------

    @action(category=30101)
    def feed(self, **kwargs):
        return True

    # search -------------------------------------------------------------------

    def __query__(self):
        self.logger.info(f"__query__()")
        return self.__client__.query()

    def __history__(self):
        self.logger.info(f"__history__()")
        if self.addNewQueryItem():
            return self.addItems(self.__client__.history())
        return False

    def __search__(self, query):
        self.logger.info(f"__search__(query={query})")
        return self.addDirectory(self.__client__.search(query), **query)

    @action(category=30102)
    def search(self, **kwargs):
        self.logger.info(f"search(kwargs={kwargs})")
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
    plugin = IVPlugin(url, int(handle))
    plugin.logger.info(f"dispatch(url='{url}', handle='{handle}', query='{query}', args={args})")
    plugin.dispatch(**parseQuery(query))


if __name__ == "__main__":
    dispatch(*argv)
