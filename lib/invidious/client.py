# -*- coding: utf-8 -*-


from iapc import Client
from iapc.tools import getSetting, selectDialog, setSetting, Logger

from invidious.items import (
    Folder, Folders
)


# ------------------------------------------------------------------------------
# InvidiousClient

class InvidiousClient(object):

    def __init__(self):
        self.logger = Logger(component="client")
        self.__client__ = Client()
        self.__subFolders__ = self.__client__.subFolders()
        self.__home__ = self.__client__.home()

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
        return Folders(
            [
                folder for folder in self.__home__
                if (
                    getSetting(f"home.{folder['type']}", bool)
                    if folder.get("optional", False)
                    else True
                )
            ],
            category="Invidious"
        )

    # subFolders ---------------------------------------------------------------

    def subFolders(self, type, **kwargs):
        return Folders(self.__subFolders__[type], **kwargs)

    # pushQuery ----------------------------------------------------------------

    def pushQuery(self, query):
        return self.__client__.pushQuery(query)
