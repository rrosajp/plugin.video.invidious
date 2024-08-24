# -*- coding: utf-8 -*-


from datetime import date

from iapc.tools import localizedString


# ------------------------------------------------------------------------------

def __date__(timestamp):
    if isinstance(timestamp, int):
        return date.fromtimestamp(timestamp)
    return timestamp


# ------------------------------------------------------------------------------
# Video

class VideoThumbnails(object):

    def __new__(cls, thumbnails=None):
        return super(VideoThumbnails, cls).__new__(cls) if thumbnails else None

    def __init__(self, thumbnails):
        if isinstance(thumbnails[0], list):
            thumbnails = thumbnails[0]
        for thumbnail in thumbnails:
            if isinstance(thumbnail, list):
                thumbnail = thumbnail[0]
            setattr(self, thumbnail["quality"], thumbnail["url"])


class Video(dict):

    def __init__(self, item):
        duration = (
            -1 if (live := item.get("liveNow", False))
            else item["lengthSeconds"]
            #else item.get("lengthSeconds", -1)
        )
        thumbnails = VideoThumbnails(item.get("videoThumbnails"))
        likes, likesText = item.get("likeCount", 0), item.get("likeCountText")
        if not likesText and likes:
            likesText = localizedString(30303).format(likes)
        views, viewsText = item.get("viewCount", 0), item.get("viewCountText")
        if not viewsText and views:
            viewsText = localizedString(30302).format(views)
        published = item["published"]
        publishedDate = __date__(published)
        publishedText = localizedString(30301).format(
            f"{publishedText} ({publishedDate})"
            if (publishedText := item.get("publishedText"))
            else publishedDate
        )
        super(Video, self).__init__(
            type="video",
            videoId=item["videoId"],
            title=item["title"],
            description=(item.get("description") or None),
            channelId=item["authorId"],
            channel=item["author"],
            duration=duration,
            live=live,
            thumbnail=getattr(thumbnails, "high", None),
            likes=likes,
            likesText=likesText,
            views=views,
            viewsText=viewsText,
            published=published,
            publishedDate=f"{publishedDate}",
            publishedText=publishedText,
            url=item.get("dashUrl")
        )


# ------------------------------------------------------------------------------
# Channel

class Channel(dict):

    def __init__(self, item):
        super(Channel, self).__init__(
            type="channel",
        )


# ------------------------------------------------------------------------------
# Playlist

class Playlist(dict):

    def __init__(self, item):
        super(Playlist, self).__init__(
            type="playlist",
        )


# ------------------------------------------------------------------------------

__itemTypes__ = {
    "video": Video,
    "channel": Channel,
    "playlist": Playlist
}

def extractItems(items):
    return [__itemTypes__[item["type"]](item) for item in items]
