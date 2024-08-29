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
        published = item["published"]
        publishedDate = f"{__date__(published)}"
        publishedText = localizedString(30301).format(
            f"{publishedText} ({publishedDate})"
            if (publishedText := item.get("publishedText"))
            else publishedDate
        )
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
            subsText=subsText
        )


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

__itemTypes__ = {
    "video": IVVideo,
    "channel": IVChannel,
    "playlist": IVPlaylist
}

def extractIVItems(items):
    return [__itemTypes__[item["type"]](item) for item in items]
