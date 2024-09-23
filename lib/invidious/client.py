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

    def __init__(self, logger):
        self.logger = logger.getLogger(f"{logger.component}.client")
        self.__client__ = Client()

    # video --------------------------------------------------------------------

    @instance
    def video(self, **kwargs):
        if (video := self.__client__.video(**kwargs)):
            return (Video(video).makeItem(video["url"]), video["manifestType"])
        return (None, None)

    # channel ------------------------------------------------------------------

    # playlist -----------------------------------------------------------------

    # home ---------------------------------------------------------------------

    def home(self):
        return Folders(self.__client__.folders())

    # feed ---------------------------------------------------------------------

    # popular ------------------------------------------------------------------

    @instance
    def popular(self, **kwargs):
        if (videos := self.__client__.instance.popular(**kwargs)):
            return Videos(videos, **kwargs)

    # trending -----------------------------------------------------------------

    # search -------------------------------------------------------------------
