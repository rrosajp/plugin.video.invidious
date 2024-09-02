# -*- coding: utf-8 -*-


from datetime import date

from iapc.tools import localizedString


# ------------------------------------------------------------------------------

def __date__(timestamp):
    if isinstance(timestamp, int):
        return date.fromtimestamp(timestamp)
    return timestamp


def __url__(url):
    return f"https:{url}" if url.startswith("//") else url


class Thumbnails(object):

    def __new__(cls, thumbnails=None):
        return super(Thumbnails, cls).__new__(cls) if thumbnails else None

    def __getattribute__(self, name):
        return __url__(super(Thumbnails, self).__getattribute__(name))


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


class IVVideo(dict):

    def __init__(self, item):
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
        likes, likesText = item.get("likeCount", 0), item.get("likeCountText")
        if not likesText and likes:
            likesText = localizedString(30303).format(likes)
        views, viewsText = item.get("viewCount", 0), item.get("viewCountText")
        if not viewsText and views:
            viewsText = localizedString(30302).format(views)
        if (published := item.get("published")):
            publishedDate = f"{__date__(published)}"
            publishedText = localizedString(30301).format(
                f"{publishedText} ({publishedDate})"
                if (publishedText := item.get("publishedText"))
                else publishedDate
            )
        else:
            publishedDate = publishedText = None
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


class IVChannel(dict):

    __tabs__ = {
        "playlists": {"title": 30203},
        "streams": {"title": 30204},
        "shorts": {"title": 30205}
    }

    def __init__(self, item):
        thumbnails = ChannelThumbnails(item.get("authorThumbnails"))
        subs, subsText = item.get("subCount", 0), item.get("subCountText")
        if not subsText and subs:
            subsText = localizedString(30304).format(subs)
        super(IVChannel, self).__init__(
            type="channel",
            channelId=item["authorId"],
            channel=item["author"],
            description=(item.get("description") or None),
            thumbnail=getattr(thumbnails, "512", None),
            subs=subs,
            subsText=subsText,
            tabs=[
                dict(tab, type=type)
                for type, tab in self.__tabs__.items()
                if type in item.get("tabs", [])
            ]
        )

    def __repr__(self):
        return f"IVChannel({self['channel']})"


# ------------------------------------------------------------------------------
# IVPlaylist

class IVPlaylist(dict):

    def __init__(self, item):
        thumbnail = (
            __url__(url) if (url := item.get("playlistThumbnail")) else None
        )
        views, viewsText = item.get("viewCount", 0), item.get("viewCountText")
        if not viewsText and views:
            viewsText = localizedString(30302).format(views)
        videos, videosText = item.get("videoCount", 0), item.get("videoCountText")
        if not videosText and videos:
            videosText = localizedString(30305).format(videos)
        if (updated := item.get("updated")):
            updatedDate = f"{__date__(updated)}"
            updatedText = localizedString(30306).format(
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
# IVPlaylistVideos

class IVPlaylistVideos(IVPlaylist):

    def __init__(self, item):
        super(IVPlaylistVideos, self).__init__(item)
        self["videos"] = [IVVideo(video) for video in item["videos"]]


# ------------------------------------------------------------------------------
# IVChannelVideos

class IVChannelVideos(dict):

    def __init__(self, channel, items):
        super(IVChannelVideos, self).__init__(
            channel=channel,
            continuation=items.get("continuation"),
            videos=[IVVideo(video) for video in items["videos"]]
        )


# ------------------------------------------------------------------------------
# IVChannelPlaylists

class IVChannelPlaylists(dict):

    def __init__(self, channel, items):
        super(IVChannelPlaylists, self).__init__(
            channel=channel,
            continuation=items.get("continuation"),
            playlists=[IVPlaylist(playlist) for playlist in items["playlists"]]
        )


# ------------------------------------------------------------------------------

__itemTypes__ = {
    "video": IVVideo,
    "channel": IVChannel,
    "playlist": IVPlaylist
}

def extractIVItems(items):
    return [__itemTypes__[item["type"]](item) for item in items]
