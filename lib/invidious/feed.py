# -*- coding: utf-8 -*-


from time import time

from iapc import public
from nuttig import containerRefresh, localizedString, notify, ICONINFO

from invidious.extract import IVChannel, IVVideo
from invidious.persistence import IVFeedChannels
from invidious.utils import confirm

# ------------------------------------------------------------------------------
# IVFeed

class IVFeed(object):

    def __init__(self, logger, instance, timeout=1800):
        self.logger = logger.getLogger(f"{logger.component}.feed")
        self.__instance__ = instance

    def __setup__(self):
        pass

    def __stop__(self):
        self.__instance__ = None
        self.logger.info("stopped")
