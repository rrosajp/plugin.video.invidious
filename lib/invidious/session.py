# -*- coding: utf-8 -*-


from concurrent.futures import ThreadPoolExecutor
from requests import Session, Timeout

from iapc.tools import buildUrl


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
        else:
            response.raise_for_status()
            return response.json()

    def map_get(self, urls, **kwargs):
        self.logger.info(f"map_get(urls={urls}, kwargs={kwargs})")
        def __map_get__(url):
            return self.get(url, **kwargs) # maybe swallow exceptions
        return self.__pool__.map(__map_get__, urls)

