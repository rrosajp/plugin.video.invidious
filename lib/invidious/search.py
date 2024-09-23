# -*- coding: utf-8 -*-


from collections import deque, OrderedDict

from iapc import public
from nuttig import (
    containerRefresh, getSetting, inputDialog, localizedString,
    notify, selectDialog, ICONINFO
)

from invidious.persistence import IVSearchHistory
from invidious.utils import confirm


#-------------------------------------------------------------------------------

queryType = OrderedDict(
    (
        (None, 42230),
        ("all", 42211),
        ("video", 42212),
        ("channel", 42213),
        ("playlist", 42214),
        ("movie", 42215),
        ("show", 42216)
    )
)


querySort = OrderedDict(
    (
        (None, 42230),
        ("relevance", 42221),
        ("date", 42222),
        ("views", 42223),
        ("rating", 42224)
    )
)


#-------------------------------------------------------------------------------
# IVSearch

class IVSearch(object):

    def __init__(self, logger, instance):
        self.logger = logger.getLogger(f"{logger.component}.search")
        self.__instance__ = instance

    def __setup__(self):
        pass

    def __stop__(self):
        self.__instance__ = None
        self.logger.info("stopped")
