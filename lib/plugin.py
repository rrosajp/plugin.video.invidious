# -*- coding: utf-8 -*-


from sys import argv
from urllib.parse import urlencode

from inputstreamhelper import Helper

from iapc.tools import action, executeBuiltin, getSetting, openSettings, parseQuery, Plugin

from invidious.client import IVClient
from invidious.utils import moreItem, settingsItem


# ------------------------------------------------------------------------------
# IVPlugin

class IVPlugin(Plugin):

    def __init__(self, *args, **kwargs):
        super(IVPlugin, self).__init__(*args, **kwargs)
        self.__client__ = IVClient()

    # helpers ------------------------------------------------------------------

    #def addMore(self, more, **kwargs):
    #    if more is True:
    #        kwargs["page"] = int(kwargs.get("page", 1)) + 1
    #    else:
    #        kwargs["continuation"] = more
    #    return self.addItem(
    #        moreItem(self.url, action=self.action, **kwargs)
    #    )

    def addDirectory(self, items, *args, **kwargs):
        if super(IVPlugin, self).addDirectory(items, *args):
            #if (more := getattr(items, "more", None)):
            #    return self.addMore(more, **kwargs)
            return True
        return False

    def addSettings(self):
        if getSetting("home.settings", bool):
            return self.addItem(
                settingsItem(self.url, action="settings", instance=False)
            )
        return True

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

    # home ---------------------------------------------------------------------

    @action(category=30000)
    def home(self, **kwargs):
        if self.addDirectory(self.__client__.home()):
            return self.addSettings()
        return False

    # feed ---------------------------------------------------------------------

    @action(category=30101)
    def feed(self, **kwargs):
        return True

    # search -------------------------------------------------------------------

    @action(category=30102)
    def search(self, **kwargs):
        self.logger.info(f"search(kwargs={kwargs})")
        if ((items := self.__client__.search(**kwargs)) is not None):
            return self.addDirectory(items, **kwargs)
        return False

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
