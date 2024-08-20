# -*- coding: utf-8 -*-


from sys import argv
from urllib.parse import urlencode

from inputstreamhelper import Helper

from iapc import Client
from iapc.tools import action, parseQuery, Plugin

from scripts import selectPublicInstance


# ------------------------------------------------------------------------------
# InvidiousPlugin

class InvidiousPlugin(Plugin):

    def __init__(self, *args, **kwargs):
        super(InvidiousPlugin, self).__init__(*args, **kwargs)
        self.__client__ = Client()

    def dispatch(self, **kwargs):
        if (
            self.__client__.instance() or
            (selectPublicInstance() and self.__client__.instance())
        ):
            return super(InvidiousPlugin, self).dispatch(**kwargs)
        self.endDirectory(False)
        return False

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
        return True


# __main__ ---------------------------------------------------------------------

def dispatch(url, handle, query, *args):
    InvidiousPlugin(url, int(handle)).dispatch(**parseQuery(query))


if __name__ == "__main__":
    dispatch(*argv)
