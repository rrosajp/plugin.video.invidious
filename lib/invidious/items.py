# -*- coding: utf-8 -*-


from urllib.parse import quote_plus

from iapc.tools import (
    buildUrl, getAddonId, getSetting, localizedString, maybeLocalize, ListItem
)
from iapc.tools.objects import List, Object


# ------------------------------------------------------------------------------
# Items

class Item(Object):

    __menus__ = []

    @classmethod
    def menus(cls, **kwargs):
        return [
            (
                maybeLocalize(label).format(**kwargs),
                action.format(
                    addonId=getAddonId(),
                    **{key: quote_plus(value) for key, value in kwargs.items()}
                )
            )
            for label, action, *settings in cls.__menus__
            if all(getSetting(*iargs) == ires for iargs, ires in settings)
        ]

    @property
    def thumbnail(self):
        return self.get("thumbnail", self.__thumbnail__)

    @property
    def icon(self):
        return self.get("icon", self.__thumbnail__)


class Items(List):

    __ctor__ = Item

    def __init__(self, items, continuation=None, limit=0, **kwargs):
        super(Items, self).__init__(items, **kwargs)
        self.more = continuation or ((len(self) >= limit) if limit else False)


class Contents(Items):

    def __init__(self, items, **kwargs):
        super(Contents, self).__init__(
            items["contents"],
            continuation=items["continuation"],
            content="videos",
            **kwargs
        )


# ------------------------------------------------------------------------------
# Folders

class Folder(Item):

    __thumbnail__ = "DefaultFolder.png"

    @property
    def action(self):
        return self.get("action", self.type)

    @property
    def plot(self):
        if (plot := self.get("plot")):
            return maybeLocalize(plot)

    @property
    def art(self):
        return dict(
            {"icon": self.icon, "poster": self.thumbnail}, **self.get("art", {})
        )

    def getItem(self, url, **kwargs):
        title = maybeLocalize(self.title)
        return ListItem(
            title,
            buildUrl(url, action=self.action, **dict(self.kwargs, **kwargs)),
            isFolder=True,
            infoLabels={
                "video": {
                    "title": title,
                    "plot": self.plot or title
                }
            },
            **self.art
        )


class Folders(Items):

    __ctor__ = Folder
