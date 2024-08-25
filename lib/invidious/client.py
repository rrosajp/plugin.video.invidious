# -*- coding: utf-8 -*-


from functools import wraps

from iapc import Client
from iapc.tools import getSetting, selectDialog, setSetting, Logger

from invidious.items import buildItems, Folders, Video


# instance ---------------------------------------------------------------------

def instance(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if (
            self.__client__.instance() or
            (self.__client__.selectInstance() and self.__client__.instance())
        ):
            return func(self, *args, **kwargs)
    return wrapper


# ------------------------------------------------------------------------------
# IVClient

class IVClient(object):

    def __init__(self):
        self.logger = Logger(component="client")
        self.__client__ = Client()

    # play ---------------------------------------------------------------------

    @instance
    def play(self, **kwargs):
        self.logger.info(f"play(kwargs={kwargs})")
        if (video := self.__client__.play(**kwargs)):
            return (Video(video).makeItem(video["url"]), video["manifestType"])
        return (None, None)

    # home ---------------------------------------------------------------------

    def home(self):
        return Folders(self.__client__.home())

    # feed ---------------------------------------------------------------------

    @instance
    def feed(self, **kwargs):
        self.logger.info(f"feed(kwargs={kwargs})")

    # search -------------------------------------------------------------------

    @instance
    def search(self, **kwargs):
        self.logger.info(f"search(kwargs={kwargs})")
        if ((items := self.__client__.search(**kwargs)) is not None):
            return buildItems(items, limit=20)
