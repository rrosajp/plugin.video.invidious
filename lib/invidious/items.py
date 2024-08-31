# -*- coding: utf-8 -*-


from urllib.parse import quote_plus

from iapc.tools import (
    buildUrl, getAddonId, getSetting, localizedString, maybeLocalize, ListItem
)
from iapc.tools.objects import List, Object

from invidious.search import queryType, querySort


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

    def __infos__(self, *args):
        for arg in args:
            if (attr := getattr(self, arg, None)):
                yield f"{attr}"

    @property
    def thumbnail(self):
        return self.get("thumbnail", self.__thumbnail__)

    @property
    def poster(self):
        return self.get("poster", self.__thumbnail__)

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
        super(Contents, self).__init__(items, content="videos", **kwargs)


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
            {"poster": self.poster, "icon": self.icon}, **self.get("art", {})
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


# ------------------------------------------------------------------------------
# Queries

class Query(Item):

    __menus__ = [
        (40432, "RunScript({addonId},updateQueryType,{q})"),
        (40422, "RunScript({addonId},updateQuerySort,{q})"),
        (50503, "RunScript({addonId},removeQuery,{q})"),
        (50504, "RunScript({addonId},clearHistory)")
    ]

    __thumbnail__ = "DefaultAddonsSearch.png"

    __thumbnails__ = {
        "all": "DefaultAddonsSearch.png",
        "video": "DefaultAddonVideo.png",
        "channel": "DefaultArtist.png",
        "playlist": "DefaultPlaylist.png",
        "movie": "DefaultMovies.png",
        "show": "DefaultTVShows.png"
    }

    @property
    def thumbnail(self):
        return self.__thumbnails__.get(self.type, self.__thumbnail__)

    def getItem(self, url):
        return ListItem(
            self.q,
            buildUrl(
                url,
                action="search",
                q=self.q,
                type=self.type,
                sort=self.sort,
                page=self.page
            ),
            isFolder=True,
            infoLabels={
                "video": {
                    "title": self.q,
                    "plot": self.q
                }
            },
            contextMenus=self.menus(
                q=self.q,
                _type_=localizedString(queryType[self.type]),
                _sort_=localizedString(querySort[self.sort])
            ),
            thumb=self.thumbnail
        )


class Queries(Items):

    __ctor__ = Query


# ------------------------------------------------------------------------------
# Videos

class Video(Item):

    __thumbnail__ = "DefaultAddonVideo.png"

    @property
    def title(self):
        #if self.live:
        if self.live or (not self.duration):
            return " ".join(("[COLOR red](₍.₎)[/COLOR]", self.get("title")))
        return self.get("title")

    @property
    def _infos_(self):
        return " • ".join(list(self.__infos__("viewsText", "likesText")))

    @property
    def infos(self):
        return "\n".join(list(self.__infos__("_infos_", "publishedText")))

    @property
    def plot(self):
        return "\n\n".join(
            self.__infos__("title", "channel", "infos", "description")
        )

    def makeItem(self, path):
        return ListItem(
            self.title,
            path,
            infoLabels={
                "video": {
                    "mediatype": "video",
                    "title": self.title,
                    "plot": self.plot
                }
            },
            streamInfos={
                "video": {
                    "duration": self.duration
                }
            },
            thumb=self.thumbnail
        )

    def getItem(self, url):
        return self.makeItem(buildUrl(url, action="play", videoId=self.videoId))


class Videos(Contents):

    __ctor__ = Video


# ------------------------------------------------------------------------------
# Channels

class Channel(Item):

    __thumbnail__ = "DefaultArtist.png"

    @property
    def plot(self):
        return "\n\n".join(
            self.__infos__("channel", "subsText", "description")
        )

    def getItem(self, url):
        return ListItem(
            self.channel,
            buildUrl(url, action="channel", channelId=self.channelId),
            isFolder=True,
            infoLabels={
                "video": {
                    "title": self.channel,
                    "plot": self.plot
                }
            },
            thumb=self.thumbnail
        )


class Channels(Contents):

    __ctor__ = Channel


# ------------------------------------------------------------------------------
# Playlists

class Playlist(Item):

    __thumbnail__ = "DefaultPlaylist.png"

    @property
    def _infos_(self):
        return " • ".join(list(self.__infos__("viewsText", "videosText")))

    @property
    def infos(self):
        return "\n".join(list(self.__infos__("_infos_", "updatedText")))

    @property
    def plot(self):
        return "\n\n".join(
            self.__infos__("title", "channel", "infos", "description")
        )

    def getItem(self, url):
        return ListItem(
            self.title,
            buildUrl(url, action="playlist", playlistId=self.playlistId),
            isFolder=True,
            infoLabels={
                "video": {
                    "title": self.title,
                    "plot": self.plot
                }
            },
            thumb=self.thumbnail
        )


class Playlists(Contents):

    __ctor__ = Playlist


# ------------------------------------------------------------------------------
# MixBag

class MixBag(Contents):

    __ctor__ = None

    __itemTypes__ = {
        "video": Video,
        "channel": Channel,
        "playlist": Playlist
    }

    def __init__(self, items, **kwargs):
        super(MixBag, self).__init__(
            [self.__itemTypes__[item["type"]](item) for item in items],
            **kwargs
        )

