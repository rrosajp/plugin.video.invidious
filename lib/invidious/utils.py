# -*- coding: utf-8 -*-


from iapc.tools import localizedString, ListItem, buildUrl, getMedia


# misc useful items ------------------------------------------------------------

def __makeItem__(label, url, art=None, isFolder=True, **kwargs):
    label = localizedString(label)
    return ListItem(
        label,
        buildUrl(url, **kwargs),
        isFolder=isFolder,
        isPlayable=False,
        infoLabels={"video": {"title": label, "plot": label}},
        poster=art,
        icon=art
    )


# settings item
def settingsItem(url, **kwargs):
    return __makeItem__(
        30103, url, "icons/settings/system.png", isFolder=False, **kwargs
    )


# newSearch item
def newSearchItem(url, **kwargs):
    return __makeItem__(30801, url, "DefaultAddSource.png", **kwargs)


# more item
__more_art__ = getMedia("more")

def moreItem(url, **kwargs):
    return __makeItem__(30802, url, __more_art__, **kwargs)
