# -*- coding: utf-8 -*-


from nuttig import getMedia


# folders ----------------------------------------------------------------------

__feed_art__ = getMedia("feed")

__folders__ = {
    "folders": {
        "popular": {
            "title": 30104,
            "setting": "home.popular"
        },
        "trending": {
            "title": 30105,
            "setting": "home.trending",
            "folders": {
                "music": {
                    "action": "trending",
                    "title": 30111,
                    "art": {
                        "poster": "DefaultAddonMusic.png",
                        "icon": "DefaultAddonMusic.png"
                    },
                    "kwargs": {"type": "music"}
                },
                "gaming": {
                    "action": "trending",
                    "title": 30112,
                    "art": {
                        "poster": "DefaultAddonGame.png",
                        "icon": "DefaultAddonGame.png"
                    },
                    "kwargs": {"type": "gaming"}
                },
                "movies": {
                    "action": "trending",
                    "title": 30113,
                    "art": {
                        "poster": "DefaultMovies.png",
                        "icon": "DefaultMovies.png"
                    },
                    "kwargs": {"type": "movies"}
                }
            }
        },
        "feed": {
            "title": 30101,
            "setting": "home.feed",
            "art": {
                "poster": __feed_art__,
                "icon": __feed_art__
            }
        },
#        "explore": {
#            "title": 30106,
#            "setting": "home.explore",
#            "art": {
#                "poster": "DefaultAddSource.png",
#                "icon": "DefaultAddSource.png"
#            },
#            "folders": {
#                "popular": {
#                    "title": 30104,
#                    "setting": "explore.popular"
#                },
#                "trending": {
#                    "title": 30105,
#                    "setting": "explore.trending",
#                    "folders": {
#                        "music": {
#                            "action": "trending",
#                            "title": 30111,
#                            "art": {
#                                "poster": "DefaultAddonMusic.png",
#                                "icon": "DefaultAddonMusic.png"
#                            },
#                            "kwargs": {"type": "music"}
#                        },
#                        "gaming": {
#                            "action": "trending",
#                            "title": 30112,
#                            "art": {
#                                "poster": "DefaultAddonGame.png",
#                                "icon": "DefaultAddonGame.png"
#                            },
#                            "kwargs": {"type": "gaming"}
#                        },
#                        "movies": {
#                            "action": "trending",
#                            "title": 30113,
#                            "art": {
#                                "poster": "DefaultMovies.png",
#                                "icon": "DefaultMovies.png"
#                            },
#                            "kwargs": {"type": "movies"}
#                        }
#                    }
#                }
#            }
#        },
        "search": {
            "title": 30102,
            "art": {
                "poster": "DefaultAddonsSearch.png",
                "icon": "DefaultAddonsSearch.png"
            }
        }
    }
}


class Folder(dict):

    def __init__(self, action, folder):
        return super(Folder, self).__init__(
            title=folder["title"],
            action=folder.get("action", action),
            setting=folder.get("setting"),
            art=folder.get("art", {}),
            kwargs=folder.get("kwargs", {})
        )

def getFolders(*paths):
    folders = __folders__["folders"]
    for path in paths:
        folders = folders.get(path, {}).get("folders", {})
    return [Folder(*item) for item in folders.items()]
