# -*- coding: utf-8 -*-


from functools import wraps

from iapc import Client
from nuttig import Logger

from invidious.items import (
    FeedChannels, Folders, Playlists, Queries, Results, Video, Videos
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
        if (video := self.__client__.play(**kwargs)):
            return (Video(video).makeItem(video["url"]), video["manifestType"])
        return (None, None)

    # channel ------------------------------------------------------------------

    @instance
    def tabs(self, **kwargs):
        if (tabs := self.__client__.tabs(**kwargs)):
            return Folders(tabs, **kwargs)

    @instance
    def tab(self, key, **kwargs):
        videos = self.__client__.tab(key, **kwargs)
        return Videos(
            videos["videos"],
            continuation=videos["continuation"],
            category=videos["channel"]
        )

    @instance
    def playlists(self, **kwargs):
        playlists = self.__client__.playlists(**kwargs)
        return Playlists(
            playlists["playlists"],
            continuation=playlists["continuation"],
            category=playlists["channel"]
        )

    # playlist -----------------------------------------------------------------

    @instance
    def playlist(self, **kwargs):
        playlist = self.__client__.playlist(**kwargs)
        return Videos(
            playlist["videos"], limit=200, category=playlist["title"]
        )

    # home ---------------------------------------------------------------------

    def home(self):
        return Folders(self.__client__.folders())

    # feed ---------------------------------------------------------------------

    @instance
    def feed(self, limit=19, **kwargs):
        return Videos(self.__client__.feed.feed(limit, **kwargs), limit=limit)

    @instance
    def channels(self):
        return FeedChannels(self.__client__.feed.channels())

    # explore ------------------------------------------------------------------

    #def explore(self):
    #    return Folders(self.__client__.folders("explore"))

    # popular ------------------------------------------------------------------

    @instance
    def popular(self, **kwargs):
        return Videos(self.__client__.popular(**kwargs), **kwargs)

    # trending -----------------------------------------------------------------

    @instance
    def trending(self, folders=False, **kwargs):
        if folders:
            #return Folders(self.__client__.folders("explore", "trending"))
            return Folders(self.__client__.folders("trending"))
        return Videos(self.__client__.trending(**kwargs), **kwargs)

    # search -------------------------------------------------------------------

    def query(self):
        return self.__client__.search.query()


    def history(self):
        return Queries(self.__client__.search.history())

    @instance
    def search(self, query):
        return Results(
            self.__client__.search.search(query), limit=20, category=query["q"]
        )
