# -*- coding: utf-8 -*-


from functools import wraps

from iapc import Client
from iapc.tools import getSetting, selectDialog, setSetting, Logger

from invidious.items import Folders, MixBag, Queries, Video, Videos


# instance ---------------------------------------------------------------------

def instance(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if (
            self.__client__.instance.instance() or
            (
                self.__client__.instance.selectInstance() and
                self.__client__.instance.instance()
            )
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

    # channel ------------------------------------------------------------------

    def channel(self, **kwargs):
        self.logger.info(f"channel(kwargs={kwargs})")
        channel = self.__client__.channel(**kwargs)
        return Videos(
            channel["videos"],
            continuation=channel["continuation"],
            category=channel["channel"]
        )

    # playlist -----------------------------------------------------------------

    def playlist(self, **kwargs):
        self.logger.info(f"playlist(kwargs={kwargs})")
        playlist = self.__client__.playlist(**kwargs)
        return Videos(
            playlist["videos"], limit=200, category=playlist["title"]
        )

    # home ---------------------------------------------------------------------

    def home(self):
        return Folders(self.__client__.home())

    # feed ---------------------------------------------------------------------

    @instance
    def feed(self, **kwargs):
        self.logger.info(f"feed(kwargs={kwargs})")

    # search -------------------------------------------------------------------

    def query(self):
        self.logger.info(f"query()")
        return self.__client__.search.query()


    def history(self):
        self.logger.info(f"history()")
        return Queries(self.__client__.search.history())

    @instance
    def search(self, query):
        self.logger.info(f"search(query={query})")
        return MixBag(
            self.__client__.search.search(query), limit=20, category=query["q"]
        )
