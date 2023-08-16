# -*- coding: utf-8 -*-


__all__ = ["Url", "Thumbnails", "Item", "Items"]


from datetime import datetime
from urllib.parse import quote_plus

from iapc.tools import maybeLocalize, getAddonId, getSetting
from iapc.tools.objects import Type, Object, List


# ------------------------------------------------------------------------------
# Url

def Url(url):
    return f"https:{url}" if url.startswith("//") else url


# ------------------------------------------------------------------------------
# Thumbnails

class Thumbnails(object):

    def __new__(cls, thumbnails):
        return super(Thumbnails, cls).__new__(cls) if thumbnails else None


# ------------------------------------------------------------------------------
# Item

def __date__(value):
    return datetime.fromtimestamp(value) if isinstance(value, int) else value


class ItemType(Type):

    __transform__ = {"__date__": __date__}


class Item(Object, metaclass=ItemType):

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
    def plot(self):
        return self.__plot__.format(self)


# ------------------------------------------------------------------------------
# Items

class Items(List):

    __ctor__ = Item

    def __init__(self, items, continuation=None, limit=0, **kwargs):
        super(Items, self).__init__(items, content="videos", **kwargs)
        self.more = continuation or ((len(self) >= limit) if limit else False)
