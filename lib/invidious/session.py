# -*- coding: utf-8 -*-


from concurrent.futures import ThreadPoolExecutor
from requests import Session, Timeout

from nuttig import buildUrl


# ------------------------------------------------------------------------------
# IVSession

class IVSession(Session):

    def __init__(self, logger, headers=None):
        super(IVSession, self).__init__()
        self.logger = logger.getLogger(f"{logger.component}.session")
        if headers:
            self.headers.update(headers)
        self.__pool__ = ThreadPoolExecutor()

    def close(self):
        self.__pool__.shutdown(cancel_futures=True)
        super(IVSession, self).close()
        self.logger.info("closed")

    def request(self, method, url, **kwargs):
        self.logger.info(
            f"request: {method} {buildUrl(url, **kwargs.get('params', {}))}"
        )
        try:
            response = super(IVSession, self).request(method, url, **kwargs)
        except Timeout as error:
            self.logger.error(f"timeout error: {error}", notify=True)
            raise error
        else:
            response.raise_for_status()
            return response.json()

    def map_get(self, urls, **kwargs):
        # I'm making the assumption that the thread safety issues between
        # requests and urllib3 have been solved (couln't find definitive info on
        # the topic).
        # If connections issues spawn from this, I'll revert back to storing
        # the session on a per thread basis in the instance (threading.local())
        # and using one session per connection (which is a waste).
        def __map_get__(url):
            try:
                return self.get(url, **kwargs)
            except Exception:
                # ignore exceptions ???
                return None
        return self.__pool__.map(__map_get__, urls)

