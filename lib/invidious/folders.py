# -*- coding: utf-8 -*-


from iapc.tools import getMedia


# subFolders -------------------------------------------------------------------

__subFolders__ = {
    "search": {
        "videos": {
            "title": 30201,
            "art": {
                "poster": "DefaultAddonVideo.png",
                "icon": "DefaultAddonVideo.png"
            },
            "kwargs": {"type": "videos"}
        },
        "channels": {
            "title": 30202,
            "art": {
                "poster": "DefaultArtist.png",
                "icon": "DefaultArtist.png"
            },
            "kwargs": {"type": "channels"}
        },
        "playlists": {
            "title": 30203,
            "art": {
                "poster": "DefaultPlaylist.png",
                "icon": "DefaultPlaylist.png"
            },
            "kwargs": {"type": "playlists"}
        }
    }
}

subFolders = {
    type: [
        dict(folder, type=type, subType=subType)
        for subType, folder in folders.items()
    ]
    for type, folders in __subFolders__.items()
}


# home -------------------------------------------------------------------------

__feed_art__ = getMedia("feed")

__home__ = {
    "feed": {
        "title": 30101,
        "optional": True,
        "art": {
            "poster": __feed_art__,
            "icon": __feed_art__
        }
    },
    "search": {
        "title": 30102,
        "art": {
            "poster": "DefaultAddonsSearch.png",
            "icon": "DefaultAddonsSearch.png"
        }
    }
}

home = [
    dict(folder, type=type)
    for type, folder in __home__.items()
]
