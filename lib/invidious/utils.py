# -*- coding: utf-8 -*-


from iapc.tools import (
    localizedString, ListItem, buildUrl, getMedia, yesnoDialog
)


# misc useful items ------------------------------------------------------------

def __makeItem__(label, url, art=None, isFolder=True, **kwargs):
    label = localizedString(label)
    return ListItem(
        label,
        buildUrl(url, **kwargs),
        isFolder=isFolder,
        isPlayable=False,
        infoLabels={"video": {"title": label, "plot": label}},
        thumb=art,
        poster=art,
        icon=art
    )


# settings item
def settingsItem(url, **kwargs):
    return __makeItem__(
        30103, url, art="icons/settings/system.png", isFolder=False, **kwargs
    )


# newQuery item
def newQueryItem(url, **kwargs):
    return __makeItem__(30801, url, art="DefaultAddSource.png", **kwargs)


# channels item
def channelsItem(url, **kwargs):
    return __makeItem__(30202, url, art="DefaultArtist.png", **kwargs)


# more item
__more_art__ = getMedia("more")

def moreItem(url, **kwargs):
    return __makeItem__(30802, url, art=__more_art__, **kwargs)


# dialogs ----------------------------------------------------------------------

def confirm():
    return yesnoDialog(localizedString(90001))
