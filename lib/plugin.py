# -*- coding: utf-8 -*-


from sys import argv
from urllib.parse import urlencode

from inputstreamhelper import Helper

from iapc.tools import action, getSetting, openSettings, parseQuery, Plugin

from invidious.client import InvidiousClient
from invidious.utils import moreItem, newSearchItem, settingsItem


# ------------------------------------------------------------------------------
# InvidiousPlugin

class InvidiousPlugin(Plugin):

    def __init__(self, *args, **kwargs):
        super(InvidiousPlugin, self).__init__(*args, **kwargs)
        self.__client__ = InvidiousClient()

    def dispatch(self, **kwargs):
        if self.__client__.instance():
            return super(InvidiousPlugin, self).dispatch(**kwargs)
        self.endDirectory(False)
        return False

    # helpers ------------------------------------------------------------------

    #def addDirectory(self, items, *args, **kwargs):
    #    if super(MyPlugin, self).addDirectory(items, *args):
    #        if (more := getattr(items, "more", None)):
    #            return self.addMore(more, **kwargs)
    #        return True
    #    return False

    #def addMore(self, more, **kwargs):
    #    if more is True:
    #        kwargs["page"] = int(kwargs.get("page", 1)) + 1
    #    else:
    #        kwargs["continuation"] = more
    #    return self.addItem(
    #        moreItem(self.url, action=self.action, **kwargs)
    #    )

    def addNewSearch(self, **kwargs):
        return self.addItem(
            newSearchItem(self.url, action="search", new=True, **kwargs)
        )

    def addSettings(self):
        if getSetting("home.settings", bool):
            return self.addItem(settingsItem(self.url, action="settings"))
        return True

    def playItem(
        self, item, manifestType, mimeType=None, headers=None, params=None
    ):
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
        return super(MyPlugin, self).playItem(item, mimeType=mimeType)

    # play ---------------------------------------------------------------------

    @action(directory=False)
    def play(self, **kwargs):
        self.logger.info(f"play(kwargs={kwargs})")
        return True

    # home ---------------------------------------------------------------------

    @action()
    def home(self, **kwargs):
        self.logger.info(f"home(kwargs={kwargs})")
        return self.addSettings()
        #if self.addDirectory(self.__client__.home()):
        #    return self.addSettings()
        #return False
        return True

    # settings -----------------------------------------------------------------

    @action(directory=False)
    def settings(self, **kwargs):
        openSettings()
        return True


# __main__ ---------------------------------------------------------------------

def dispatch(url, handle, query, *args):
    InvidiousPlugin(url, int(handle)).dispatch(**parseQuery(query))


if __name__ == "__main__":
    dispatch(*argv)
