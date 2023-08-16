# -*- coding: utf-8 -*-


__all__ = ["Video", "Videos"]


from iapc.tools import localizedString, ListItem, buildUrl

from .base import Url, Thumbnails, Item, Items


# ------------------------------------------------------------------------------
# Videos

class VideoThumbnails(Thumbnails):

    def __init__(self, thumbnails):
        if isinstance(thumbnails[0], list):
            thumbnails = thumbnails[0]
        for thumbnail in thumbnails:
            if isinstance(thumbnail, list):
                thumbnail = thumbnail[0]
            setattr(self, thumbnail["quality"], Url(thumbnail["url"]))


class Video(Item):
    __transform__ = {"videoThumbnails": VideoThumbnails}
    __date__ = {"published"}
    __live__ = localizedString(30059)
    __infos__ = {"mediatype": "video"}

    __menus__ = [
        (
            30033, "RunScript({addonId},playFromYouTube,{videoId})",
            (("fromyoutube", bool), True)
        ),
        (
            30037, "RunScript({addonId},playWithYouTube,{videoId})",
            (("withyoutube", bool), True)
        ),
        (30031, "RunScript({addonId},goToChannel,{authorId})"),
        (30032, "RunScript({addonId},addChannelToFavourites,{authorId})"),
        (
            30034, "RunScript({addonId},addChannelToFeed,{authorId},{author})",
            (("feed", bool), True)
        )
    ]

    @property
    def liveNow(self):
        return self.get("liveNow", False)

    @property
    def label(self):
        return self.__live__.format(self) if self.liveNow else self.title

    @property
    def infos(self):
        return dict(self.__infos__, playcount=0) if self.liveNow else self.__infos__

    @property
    def subplot(self):
        subplot = [localizedString(30053)]
        if hasattr(self, "viewCount"):
            subplot.append(localizedString(30054))
        if hasattr(self, "published"):
            subplot.append(localizedString(30055))
        return "\n".join(subplot)

    @property
    def plot(self):
        plot = ["{0.title}", self.subplot]
        if hasattr(self, "description"):
            plot.append("{0.description}")
        return "\n\n".join(plot).format(self)

    @property
    def thumbnail(self):
        return getattr(
            self.videoThumbnails, "high", "DefaultAddonVideo.png"
        )

    def makeItem(self, path):
        return ListItem(
            self.label,
            path,
            infoLabels={
                "video": dict(self.infos, title=self.title, plot=self.plot)
            },
            streamInfos={"video": {"duration": self.lengthSeconds}},
            contextMenus=self.menus(
                authorId=self.authorId,
                author=self.author,
                videoId=self.videoId
            ),
            thumb=self.thumbnail
        )

    def getItem(self, url, action):
        return self.makeItem(buildUrl(url, action=action, videoId=self.videoId))


class Videos(Items):

    __ctor__ = Video
