# -*- coding: utf-8 -*
# Copyright (c) 2019 BuildGroup Data Services Inc.
# All rights reserved.
# This software is proprietary and confidential and may not under
# any circumstances be used, copied, or distributed.
import logging
import time

from caravaggio_python_bindings import status
from coreapi import exceptions

_logger = logging.getLogger("caravaggio_python_bindings.resource")


class Resource(object):
    sec_btw_tries = 5
    """
    How much time we need to wait for the next try to do the request to
    the server if we got a HTTP_429_TOO_MANY_REQUESTS error.
    """

    def __init__(self, api, tries=12):
        self.api = api
        self.n_tries = tries

    def get_absolute_url(self, relative_url):
        return "{}{}{}".format(self.api.domain, "/" if not self.api.domain.endswith("/") else "", relative_url)

    def action(
        self,
        keys,
        params=None,
        validate=True,
        overrides=None,
        action=None,
        encoding=None,
        transform=None,
        n_tries=None,
        sec_btw_tries=None,
    ):
        n_tries = self.n_tries if n_tries is None else n_tries
        sec_btw_tries = self.sec_btw_tries if sec_btw_tries is None else sec_btw_tries
        while n_tries:
            try:
                return self.api.client.action(
                    self.api.schema,
                    keys,
                    params=params,
                    validate=validate,
                    overrides=overrides,
                    action=action,
                    encoding=encoding,
                    transform=transform,
                )
            except exceptions.ErrorMessage as error:
                if error.error.title.startswith(str(status.HTTP_429_TOO_MANY_REQUESTS)):
                    _logger.info("Throttling the request! waiting {} seconds".format(sec_btw_tries))
                    n_tries -= 1
                    time.sleep(sec_btw_tries)
                else:
                    raise error
