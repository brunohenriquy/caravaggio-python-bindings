# -*- coding: utf-8 -*
# Copyright (c) 2019 BuildGroup Data Services Inc.
# All rights reserved.
# This software is proprietary and confidential and may not under
# any circumstances be used, copied, or distributed.


class Resource(object):

    def __init__(self, api):
        self.api = api

    def get_absolute_url(self, relative_url):
        return '{}{}{}'.format(
            self.api.domain,
            "/" if not self.api.domain.endswith("/") else "",
            relative_url)

    def action(self, keys, params=None, validate=True, overrides=None,
               action=None, encoding=None, transform=None):
        return self.api.client.action(
            self.api.schema, keys, params=params, validate=validate,
            overrides=overrides, action=action, encoding=encoding,
            transform=transform)
