# -*- coding: utf-8 -*-


from iapc import Client
from iapc.tools import getSetting, selectDialog, setSetting, Logger


# ------------------------------------------------------------------------------
# InvidiousClient

class InvidiousClient(object):

    def __init__(self):
        self.logger = Logger(component="client")
        self.__client__ = Client()

    # instance -----------------------------------------------------------------

    def selectInstance(self):
        if (instances := self.__client__.instances(sort_by="location,health")):
            uri = getSetting("instance.uri", str)
            keys = list(instances.keys())
            values = list(instances.values())
            preselect = keys.index(uri) if uri in keys else -1
            index = selectDialog(values, heading=40113, preselect=preselect)
            if index >= 0:
                setSetting("instance.uri", keys[index], str)
                return True
        return False

    def instance(self):
        return (
            self.__client__.instance() or
            (self.selectInstance() and self.__client__.instance())
        )

    # home ---------------------------------------------------------------------

    def home(self):
        return []
