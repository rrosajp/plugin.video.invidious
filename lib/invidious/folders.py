# -*- coding: utf-8 -*-


from nuttig import getMedia


# folders ----------------------------------------------------------------------

__folders__ = {
    "folders": {
        "feed": {
            "title": 30101,
            "setting": "home.feed",
            "art": "icons/settings/network.png"
        },
        "popular": {
            "title": 30104,
            "setting": "home.popular",
            "art": "DefaultMusicTop100.png"
        },
        "trending": {
            "title": 30105,
            "setting": "home.trending",
            "art": "DefaultFavourites.png",
            "folders": {
                "music": {
                    "action": "trending",
                    "title": 30111,
                    "art": "DefaultAddonMusic.png",
                    "kwargs": {"type": "music"}
                },
                "gaming": {
                    "action": "trending",
                    "title": 30112,
                    "art": "DefaultAddonGame.png",
                    "kwargs": {"type": "gaming"}
                },
                "movies": {
                    "action": "trending",
                    "title": 30113,
                    "art": "DefaultMovies.png",
                    "kwargs": {"type": "movies"}
                }
            }
        },
        "search": {
            "title": 30102,
            "art": "DefaultAddonsSearch.png"
        },
#        "explore": {
#            "title": 30106,
#            "setting": "home.explore",
#            "art": "DefaultAddSource.png",
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
#                            "art": "DefaultAddonMusic.png",
#                            "kwargs": {"type": "music"}
#                        },
#                        "gaming": {
#                            "action": "trending",
#                            "title": 30112,
#                            "art": "DefaultAddonGame.png",
#                            "kwargs": {"type": "gaming"}
#                        },
#                        "movies": {
#                            "action": "trending",
#                            "title": 30113,
#                            "art": "DefaultMovies.png",
#                            "kwargs": {"type": "movies"}
#                        }
#                    }
#                }
#            }
#        }
    }
}


class Folder(dict):

    def __init__(self, action, folder):
        return super(Folder, self).__init__(
            title=folder["title"],
            action=folder.get("action", action),
            setting=folder.get("setting"),
            art=dict.fromkeys(("poster", "icon"), folder.get("art")),
            kwargs=folder.get("kwargs", {})
        )

def getFolders(*paths):
    folders = __folders__["folders"]
    for path in paths:
        folders = folders.get(path, {}).get("folders", {})
    return [Folder(*item) for item in folders.items()]
