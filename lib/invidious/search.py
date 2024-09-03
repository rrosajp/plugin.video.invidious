# -*- coding: utf-8 -*-


from collections import deque, OrderedDict

from iapc import public
from iapc.tools import (
    containerRefresh, getSetting, inputDialog, localizedString, selectDialog
)

from invidious.extract import extractIVItems
from invidious.persistence import IVSearchHistory
from invidious.utils import confirm


#-------------------------------------------------------------------------------

queryType = OrderedDict(
    (
        ("all", 30210),
        ("video", 30211),
        ("channel", 30212),
        ("playlist", 30213),
        ("movie", 30214),
        ("show", 30215),
        (None, 41429)
    )
)


querySort = OrderedDict(
    (
        ("relevance", 41420),
        ("date", 41421),
        ("views", 41422),
        ("rating", 41423),
        (None, 41429)
    )
)


#-------------------------------------------------------------------------------
# IVSearch

class IVSearch(object):

    def __init__(self, logger, instance):
        self.logger = logger.getLogger(f"{logger.component}.search")
        self.__instance__ = instance
        self.__history__ = IVSearchHistory()
        self.__cache__ = deque()

    def __q_setup__(self, setting, ordered, label):
        q_setting = list(ordered.keys())[getSetting(*setting)]
        self.logger.info(
            f"{localizedString(label)}: {localizedString(ordered[q_setting])}"
        )
        return q_setting

    def __setup__(self):
        self.__q_type__ = self.__q_setup__(
            ("query.type", int), queryType, 40431
        )
        self.__q_sort__ = self.__q_setup__(
            ("query.sort", int), querySort, 40421
        )

    def __stop__(self):
        self.__instance__ = None
        self.logger.info("stopped")

    def __q_select__(self, key, ordered, heading):
        keys = [key for key in ordered.keys() if key]
        index = selectDialog(
            [localizedString(ordered[key]) for key in keys],
            heading=heading,
            preselect=keys.index(key)
        )
        return key if index < 0 else keys[index]

    def q_type(self, type="all"):
        return self.__q_select__(type, queryType, 40431)

    def q_sort(self, sort="relevance"):
        return self.__q_select__(sort, querySort, 40421)

    # search -------------------------------------------------------------------

    @public
    def query(self, **query):
        self.logger.info(f"query(query={query}))")
        try:
            query = self.__cache__.pop()
        except IndexError:
            if (q := inputDialog(heading=30102)):
                self.__history__.record(
                    (
                        query := {
                            "q": q,
                            "type": self.__q_type__ or self.q_type(),
                            "sort": self.__q_sort__ or self.q_sort(),
                            "page": 1
                        }
                    )
                )
        return query

    @public
    def history(self):
        self.logger.info(f"history()")
        self.__cache__.clear()
        return list(reversed(self.__history__.values()))

    @public
    def search(self, query):
        self.logger.info(f"search(query={query})")
        self.__cache__.append(query)
        self.__history__.move_to_end(query["q"])
        if (items := self.__instance__.request("search", **query)):
            return extractIVItems(items)
        return []

    # --------------------------------------------------------------------------

    @public
    def updateQueryType(self, q):
        _query_ = self.__history__[q]
        _type_ = _query_["type"]
        if ((type := self.q_type(type=_type_)) != _type_):
            _query_["type"] = type
            self.__history__.record(_query_)
            containerRefresh()

    @public
    def updateQuerySort(self, q):
        _query_ = self.__history__[q]
        _sort_ = _query_["sort"]
        if ((sort := self.q_sort(sort=_sort_)) != _sort_):
            _query_["sort"] = sort
            self.__history__.record(_query_)
            containerRefresh()

    @public
    def removeQuery(self, q):
        self.__history__.remove(q)
        containerRefresh()

    @public
    def clearHistory(self):
        if confirm():
            self.__history__.clear()
            containerRefresh()
