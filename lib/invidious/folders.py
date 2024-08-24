# -*- coding: utf-8 -*-


from iapc.tools import getMedia


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
