# -*- coding: utf-8 -*-


from iapc import AddonNotAvailable, Client
from nuttig import (
    addonIsEnabled, getSetting, localizedString, okDialog, setSetting
)


# ------------------------------------------------------------------------------
# YtDlp

class YtDlp(object):

    __service_id__ = "service.yt-dlp"
    __setting_id__ = "context.fromyoutube"

    def __init__(self, logger):
        self.logger = logger.getLogger(f"{logger.component}.yt-dlp")
        self.__check__()

    def __check__(self):
        if (
            getSetting(self.__setting_id__, bool) and
            (not addonIsEnabled(self.__service_id__))
        ):
            setSetting(self.__setting_id__, False, bool)

    def __setup__(self):
        self.__check__()
        self.__enabled__ = getSetting(self.__setting_id__, bool)

    def __stop__(self):
        pass

    # play ---------------------------------------------------------------------

    def play(self, videoId):
        if self.__enabled__:
            try:
                return Client(self.__service_id__).play(
                    f"https://www.youtube.com/watch?v={videoId}"
                )
            except AddonNotAvailable:
                okDialog(localizedString(90004).format(self.__service_id__))
