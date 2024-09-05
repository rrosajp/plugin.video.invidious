# -*- coding: utf-8 -*-


from iapc import AddonNotAvailable, Client
from nuttig import getSetting, localizedString, okDialog


# ------------------------------------------------------------------------------
# YtDlp

class YtDlp(object):

    __service_id__ = "service.yt-dlp"

    def __init__(self, logger):
        self.logger = logger.getLogger(f"{logger.component}.yt-dlp")

    def __setup__(self):
        self.__fps_limit_30__ = getSetting("fps.limit.30", bool)
        self.logger.info(f"{localizedString(40321)}: {self.__fps_limit_30__}")

    def __stop__(self):
        pass

    # play ---------------------------------------------------------------------

    def play(self, videoId):
        fps = 30 if self.__fps_limit_30__ else 0
        try:
            return Client(self.__service_id__).play(
                f"https://www.youtube.com/watch?v={videoId}", fps=fps
            )
        except AddonNotAvailable:
            okDialog(localizedString(90004).format(self.__service_id__))
