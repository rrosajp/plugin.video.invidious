# -*- coding: utf-8 -*-


from datetime import date
from time import time

from nuttig import localizedString, Logger


# ------------------------------------------------------------------------------

def __date__(datestamp):
    if isinstance(datestamp, int):
        return date.fromtimestamp(datestamp)
    return datestamp


def __url__(url):
    return f"https:{url}" if url.startswith("//") else url


class Thumbnails(object):

    def __new__(cls, thumbnails=None):
        return super(Thumbnails, cls).__new__(cls) if thumbnails else None

    def __getattribute__(self, name):
        return __url__(super(Thumbnails, self).__getattribute__(name))


class Dict(dict):

    def __new__(cls, item):
        if item is not None:
            return super(Dict, cls).__new__(cls)
        return item


# ------------------------------------------------------------------------------
# IVVideo

class VideoThumbnails(Thumbnails):

    def __init__(self, thumbnails):
        if isinstance(thumbnails[0], list):
            thumbnails = thumbnails[0]
        for thumbnail in thumbnails:
            if isinstance(thumbnail, list):
                thumbnail = thumbnail[0]
            setattr(self, thumbnail["quality"], thumbnail["url"])


class IVVideo(Dict):

    def __init__(self, item, expires=1800):
        duration = (
            -1 if (live := item.get("liveNow", False))
            else item["lengthSeconds"]
            #else item.get("lengthSeconds", -1)
        )
        manifestType = "hls"
        if ((not live) or (not (url := item.get("hlsUrl")))):
            url = item.get("dashUrl")
            manifestType = "mpd"
        thumbnails = VideoThumbnails(item.get("videoThumbnails"))
        # published
        stamp, published = item.get("published", 0), item.get("publishedText")
        if stamp:
            stamp = __date__(stamp)
            published = f"{published} ({stamp})" if published else stamp
        if published:
            published = localizedString(50101).format(published)
        # views
        viewCount, views = item.get("viewCount", 0), item.get("viewCountText")
        if not views and viewCount:
            views = localizedString(50102).format(viewCount)
        # likes
        likeCount, likes = item.get("likeCount", 0), item.get("likeCountText")
        if not likes and likeCount:
            likes = localizedString(50103).format(likeCount)
        super(IVVideo, self).__init__(
            type="video",
            videoId=item["videoId"],
            title=item["title"],
            description=(item.get("description") or None),
            channelId=item["authorId"],
            channel=item["author"],
            duration=duration,
            live=live,
            url=url,
            manifestType=manifestType,
            thumbnail=getattr(thumbnails, "high", None),
            published=published,
            views=views,
            likes=likes
        )
        self.__expires__ = (int(time()) + expires)


# ------------------------------------------------------------------------------
# YtDlpVideo

class YtDlpVideo(Dict):

    def __init__(self, item):

        if (published := item["timestamp"]):
            publishedDate = f"{__date__(published)}"
            publishedText = localizedString(50101).format(
                f"{publishedText} ({publishedDate})"
                if (publishedText := item.get("publishedText"))
                else publishedDate
            )
        else:
            publishedDate = publishedText = None

        if (views := item["view_count"]):
            viewsText = localizedString(50102).format(views)
        else:
            viewsText = None

        if (likes := item["like_count"]):
            likesText = localizedString(50103).format(likes)
        else:
            likesText = None

        super(YtDlpVideo, self).__init__(
            type="video",
            videoId=item["video_id"],
            title=item["title"],
            description=(item.get("description") or None),
            channelId=item["channel_id"],
            channel=item["channel"],
            duration=item["duration"],
            live=item["is_live"],
            url=item["url"],
            manifestType=item["manifestType"],
            thumbnail=item["thumbnail"],
            likes=likes,
            likesText=likesText,
            views=views,
            viewsText=viewsText,
            published=published,
            publishedDate=publishedDate,
            publishedText=publishedText
        )


# ------------------------------------------------------------------------------
# IVChannel

class ChannelThumbnails(Thumbnails):

    def __init__(self, thumbnails):
        for thumbnail in thumbnails:
            setattr(self, str(thumbnail["height"]), thumbnail["url"])


class IVChannel(Dict):

    __tabs__ = {
        "playlists": {"title": 31100},
        "streams": {"title": 31200},
        "shorts": {"title": 31300}
    }

    def __init__(self, item):
        thumbnails = ChannelThumbnails(item.get("authorThumbnails"))

        subs, subsText = item.get("subCount", 0), item.get("subCountText")
        if not subsText and subs:
            subsText = localizedString(50201).format(subs)

        super(IVChannel, self).__init__(
            type="channel",
            channelId=item["authorId"],
            channel=item["author"],
            description=(item.get("description") or None),
            thumbnail=getattr(thumbnails, "512", None),
            subs=subs,
            subsText=subsText,
            tabs=[
                dict(tab, action=action)
                for action, tab in self.__tabs__.items()
                if action in item.get("tabs", [])
            ]
        )

    def __repr__(self):
        return f"IVChannel({self['channel']})"


# ------------------------------------------------------------------------------
# IVPlaylist

class IVPlaylist(Dict):

    def __init__(self, item):
        thumbnail = (
            __url__(url) if (url := item.get("playlistThumbnail")) else None
        )

        views, viewsText = item.get("viewCount", 0), item.get("viewCountText")
        if not viewsText and views:
            viewsText = localizedString(50102).format(views)

        videos, videosText = item.get("videoCount", 0), item.get("videoCountText")
        if not videosText and videos:
            videosText = localizedString(50301).format(videos)

        if (updated := item.get("updated")):
            updatedDate = f"{__date__(updated)}"
            updatedText = localizedString(50302).format(
                f"{updatedText} ({updatedDate})"
                if (updatedText := item.get("updatedText"))
                else updatedDate
            )
        else:
            updatedDate = updatedText = None

        super(IVPlaylist, self).__init__(
            type="playlist",
            playlistId=item["playlistId"],
            title=item["title"],
            description=(item.get("description") or None),
            channelId=item["authorId"],
            channel=item["author"],
            thumbnail=thumbnail,
            views=views,
            viewsText=viewsText,
            videos=videos,
            videosText=videosText,
            updated=updated,
            updatedDate=updatedDate,
            updatedText=updatedText
        )


# ------------------------------------------------------------------------------
# IVVideos

class IVVideos(list):

    def __init__(self, videos):
        super(IVVideos, self).__init__(
            IVVideo(video) for video in videos if video
        )


# ------------------------------------------------------------------------------
# IVPlaylistVideos

class IVPlaylistVideos(IVPlaylist):

    def __init__(self, item):
        super(IVPlaylistVideos, self).__init__(item)
        self["videos"] = [IVVideo(video) for video in item["videos"] if video]


# ------------------------------------------------------------------------------
# IVChannelVideos

class IVChannelVideos(dict):

    def __init__(self, channel, items):
        super(IVChannelVideos, self).__init__(
            channel=channel,
            continuation=items.get("continuation"),
            videos=[IVVideo(video) for video in items["videos"] if video]
        )


# ------------------------------------------------------------------------------
# IVChannelPlaylists

class IVChannelPlaylists(dict):

    def __init__(self, channel, items):
        super(IVChannelPlaylists, self).__init__(
            channel=channel,
            continuation=items.get("continuation"),
            playlists=[
                IVPlaylist(playlist)
                for playlist in items["playlists"] if playlist
            ]
        )


# ------------------------------------------------------------------------------
# IVResults

class IVResults(list):

    __types__ = {
        "video": IVVideo,
        "channel": IVChannel,
        "playlist": IVPlaylist
    }

    def __init__(self, items):
        super(IVResults, self).__init__(
            self.__types__[item["type"]](item) for item in items if item
        )
