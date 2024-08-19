# -*- coding: utf-8 -*-


from sys import argv
from urllib.parse import urlencode

from inputstreamhelper import Helper

from iapc.tools import action, parseQuery, Plugin


# ------------------------------------------------------------------------------
# InvidiousPlugin

class InvidiousPlugin(Plugin):

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

    @action()
    def play(self, **kwargs):
        return False

    # home ---------------------------------------------------------------------

    @action()
    def home(self, **kwargs):
        return True


# __main__ ---------------------------------------------------------------------

def dispatch(url, handle, query, *args):
    InvidiousPlugin(url, int(handle)).dispatch(**parseQuery(query))


if __name__ == "__main__":
    dispatch(*argv)
