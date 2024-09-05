# -*- coding: utf-8 -*-


from collections import OrderedDict

from iapc import AddonNotAvailable, Client
from nuttig import getSetting, localizedString, okDialog


# ------------------------------------------------------------------------------
# YtDlp

class YtDlp(object):

    __service_id__ = "service.yt-dlp"

    __fps_limits__ = OrderedDict(((0, 40331), (30, 40332)))

    def __init__(self, logger):
        self.logger = logger.getLogger(f"{logger.component}.yt-dlp")

    def __setup__(self):
        self.__enabled__ = getSetting("context.fromyoutube", bool)
        self.__fps__ = getSetting("fps.limit", int) if self.__enabled__ else 0
        self.logger.info(
            f"{localizedString(40321)}: "
            f"{localizedString(self.__fps_limits__[self.__fps__])}"
        )

    def __stop__(self):
        pass

    # play ---------------------------------------------------------------------

    def play(self, videoId):
        if self.__enabled__:
            try:
                return Client(self.__service_id__).play(
                    f"https://www.youtube.com/watch?v={videoId}",
                    fps=self.__fps__
                )
            except AddonNotAvailable:
                okDialog(localizedString(90004).format(self.__service_id__))
