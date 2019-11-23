# -*- coding: utf-8 -*
# Copyright (c) 2019 BuildGroup Data Services Inc.
# All rights reserved.
# This software is proprietary and confidential and may not under
# any circumstances be used, copied, or distributed.
from caravaggio_python_bindings.api import CaravaggioAPI

from caravaggio_python_bindings.tests.resource_company import CompanyResource


class MyAPI(CaravaggioAPI):
    """
    MyAPI represents a binding for the example code in Caravaggio (companies)
    """

    CARAVAGGIO_DOMAIN = "MYAPI_DOMAIN"
    CARAVAGGIO_TOKEN = "MYAPI_TOKEN"

    default_domain = "https://myservice.io"

    def get_companies(self):
        return CompanyResource(api=self)
