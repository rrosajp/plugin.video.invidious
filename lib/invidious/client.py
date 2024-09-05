# -*- coding: utf-8 -*-


from functools import wraps

from iapc import Client
from nuttig import getSetting, selectDialog, setSetting, Logger

from invidious.items import (
    FeedChannels, Folders, MixBag, Playlists, Queries, Video, Videos
)


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

    @instance
    def tabs(self, **kwargs):
        self.logger.info(f"tabs(kwargs={kwargs})")
        if (tabs := self.__client__.tabs(**kwargs)):
            return Folders(tabs, **kwargs)

    @instance
    def tab(self, key, **kwargs):
        self.logger.info(f"tab(key={key}, kwargs={kwargs})")
        videos = self.__client__.tab(key, **kwargs)
        return Videos(
            videos["videos"],
            continuation=videos["continuation"],
            category=videos["channel"]
        )

    @instance
    def playlists(self, **kwargs):
        self.logger.info(f"playlists(kwargs={kwargs})")
        playlists = self.__client__.playlists(**kwargs)
        return Playlists(
            playlists["playlists"],
            continuation=playlists["continuation"],
            category=playlists["channel"]
        )

    # playlist -----------------------------------------------------------------

    @instance
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
    def feed(self, limit=19, **kwargs):
        self.logger.info(f"feed(kwargs={kwargs})")
        return Videos(self.__client__.feed.feed(limit, **kwargs), limit=limit)

    @instance
    def channels(self):
        self.logger.info(f"channels()")
        return FeedChannels(self.__client__.feed.channels())

    # popular ------------------------------------------------------------------

    @instance
    def popular(self, **kwargs):
        self.logger.info(f"popular(kwargs={kwargs})")
        return Videos(self.__client__.popular(**kwargs), **kwargs)

    # trending -----------------------------------------------------------------

    @instance
    def trending(self, folders=False, **kwargs):
        self.logger.info(f"trending(kwargs={kwargs})")
        if folders:
            return Folders(self.__client__.trending(folders=folders))
        return Videos(self.__client__.trending(**kwargs), **kwargs)

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
