# -*- coding: utf-8 -*-


from iapc import Client
from nuttig import addonIsEnabled, localizedString, okDialog


# ------------------------------------------------------------------------------
# YtDlp

class YtDlp(object):

    def __init__(self, logger):
        self.logger = logger.getLogger(f"{logger.component}.yt-dlp")

    def __setup__(self):
        pass

    def __stop__(self):
        pass

    # play ---------------------------------------------------------------------

    __service_id__ = "service.yt-dlp"

    def play(self, videoId, yt=False, iv=False):
        if addonIsEnabled(self.__service_id__):
            return Client(self.__service_id__).play(
                f"https://www.youtube.com/watch?v={videoId}"
            )
        okDialog(localizedString(90004).format(self.__service_id__))
