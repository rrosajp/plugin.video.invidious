# -*- coding: utf-8 -*-


from collections import OrderedDict

from iapc.tools import save, Persistent


# ------------------------------------------------------------------------------
# IVSearchHistory

class IVSearchHistory(Persistent, OrderedDict):

    @save
    def record(self, query):
        self[(q := query["q"])] = query
        self.move_to_end(q)

    @save
    def remove(self, q):
        del self[q]

    @save
    def clear(self):
        super(IVSearchHistory, self).clear()

    @save
    def move_to_end(self, q):
        super(IVSearchHistory, self).move_to_end(q)
