# -*- coding: utf-8 -*-


from requests import Session, Timeout

from iapc.tools import buildUrl, notify, ICONERROR


# ------------------------------------------------------------------------------
# IVSession

class IVSession(Session):

    def __init__(self, logger, headers=None):
        super(IVSession, self).__init__()
        self.logger = logger.getLogger(f"{logger.component}.session")
        if headers:
            self.headers.update(headers)

    def request(self, method, url, **kwargs):
        self.logger.info(
            f"request: {method} {buildUrl(url, **kwargs.get('params', {}))}"
        )
        try:
            response = super(IVSession, self).request(method, url, **kwargs)
        except Timeout as error:
            self.logger.error(message := f"error: {error}")
            notify(message, icon=ICONERROR)
        else:
            response.raise_for_status()
            return response.json()
