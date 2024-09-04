# -*- coding: utf-8 -*-


from nuttig import getMedia


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
    "popular": {
        "title": 30104,
        "optional": True
    },
    "trending": {
        "title": 30105,
        "optional": True
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


# subFolders -------------------------------------------------------------------

__subFolders__ = {
    "trending": {
        "music": {
            "title": 30111,
            "art": {
                "poster": "DefaultAddonMusic.png",
                "icon": "DefaultAddonMusic.png"
            },
            "kwargs": {"type": "music"}
        },
        "gaming": {
            "title": 30112,
            "art": {
                "poster": "DefaultAddonGame.png",
                "icon": "DefaultAddonGame.png"
            },
            "kwargs": {"type": "gaming"}
        },
        "movies": {
            "title": 30113,
            "art": {
                "poster": "DefaultMovies.png",
                "icon": "DefaultMovies.png"
            },
            "kwargs": {"type": "movies"}
        }
    }
}

subFolders = {
    type: [
        dict(folder, type=type)
        for folder in folders.values()
    ]
    for type, folders in __subFolders__.items()
}
