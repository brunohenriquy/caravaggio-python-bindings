# -*- coding: utf-8 -*
# Copyright (c) 2019 BuildGroup Data Services Inc.
# All rights reserved.
# This software is proprietary and confidential and may not under
# any circumstances be used, copied, or distributed.
from caravaggio_python_bindings.resource import Resource


class CompanyResource(Resource):

    def list(self, params={}):
        return self.action(
            ['companies', 'company_search_list'],
            params=params,
            validate=False)

    def facets(self, params={}):
        return self.action(
            ['companies', 'company_search_facets'],
            params=params,
            validate=False)

    def get(self, id):
        return self.action(
            ['companies', 'company_read'], params={"id": id})

    def create(self, data):
        return self.action(
            ['companies', 'company_create'], params=data)

    def update(self, id, data, partial_update=True):
        action = "company_update" \
            if not partial_update else "company_partial_update"

        if data is None:
            raise AttributeError("The data parameter cannot be None")

        if not isinstance(data, dict):
            raise AttributeError("The data parameter must be a dictionary")

        if len(data) == 0:
            raise AttributeError("The data dictionary must contain any value")

        data["id"] = id

        return self.action(
            ['companies', action],
            validate=(not partial_update),
            params=data)

    def delete(self, id):
        """
        Remove the company from the system.

        :param id: the id of the company to be deleted
        :return:
        """
        return self.action(
            ['companies', 'company_delete'], params={"id": id})
