# -*- coding: utf-8 -*-


from collections import deque, OrderedDict

from iapc.tools import getSetting, inputDialog, localizedString, selectDialog


#-------------------------------------------------------------------------------
# IVSearch

class IVSearch(object):

    __query_type__ = OrderedDict(
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

    __query_sort__ = OrderedDict(
        (
            ("relevance", 41420),
            ("date", 41421),
            ("views", 41422),
            ("rating", 41423),
            (None, 41429)
        )
    )

    def __init__(self, logger):
        self.logger = logger.getLogger(f"{logger.component}.search")
        self.__cache__ = deque()

    def __q_setup__(self, setting, ordered, label):
        q_setting = list(ordered.keys())[getSetting(*setting)]
        self.logger.info(
            f"{localizedString(label)}: {localizedString(ordered[q_setting])}"
        )
        return q_setting

    def __setup__(self):
        self.__q_type__ = self.__q_setup__(
            ("query.type", int), self.__query_type__, 40431
        )
        self.__q_sort__ = self.__q_setup__(
            ("query.sort", int), self.__query_sort__, 40421
        )

    def __q_select__(self, key, ordered, heading):
        keys = [key for key in ordered.keys() if key]
        index = selectDialog(
            [localizedString(ordered[key]) for key in keys],
            heading=heading,
            preselect=keys.index(key)
        )
        return key if index < 0 else keys[index]

    def q_type(self, type="all"):
        return self.__q_select__(type, self.__query_type__, 40431)

    def q_sort(self, sort="relevance"):
        return self.__q_select__(sort, self.__query_sort__, 40421)

    def newSearch(self, page=1):
        self.logger.info(f"newSearch(page={page}))")
        if (q := inputDialog(heading=30102)):
            return {
                "q": q,
                "type": self.__q_type__ or self.q_type(),
                "sort": self.__q_sort__ or self.q_sort(),
                "page": page
            }

    def search(self, **kwargs):
        self.logger.info(f"search(kwargs={kwargs})")
        return self.newSearch(**kwargs)
