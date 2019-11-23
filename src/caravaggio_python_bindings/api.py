# -*- coding: utf-8 -*
# Copyright (c) 2019 BuildGroup Data Services Inc.
# All rights reserved.
# This software is proprietary and confidential and may not under
# any circumstances be used, copied, or distributed.
import os
import coreapi

from coreapi_cli import codec_plugins

from caravaggio_python_bindings.resource_users import \
    OrganizationResource, UserResource


class CaravaggioAPI(object):

    CARAVAGGIO_DOMAIN = "CARAVAGGIO_DOMAIN"
    CARAVAGGIO_TOKEN = "CARAVAGGIO_TOKEN"

    default_domain = "https://bgds.io"

    schemas = {}

    """
    Caravaggio API clients
    """

    def __init__(self, token=None, domain=None):

        if token is None:
            token = os.getenv(self.CARAVAGGIO_TOKEN, None)
            if token is None:
                raise EnvironmentError(
                    "No {0} was found in the environment"
                    ". Please, make sure you have define"
                    " the {0} environment.".format(self.CARAVAGGIO_TOKEN))

        if domain is None:
            domain = os.getenv(
                self.CARAVAGGIO_DOMAIN, self.default_domain)

        self.domain = domain

        auth = coreapi.auth.TokenAuthentication(
            scheme="Token", token=token
        )

        # Codecs are responsible for decoding a bytestring into a Document
        # instance, or for encoding a Document instance into a bytestring.
        decoders = list(codec_plugins.decoders.values())

        self.client = coreapi.Client(decoders=decoders, auth=auth)

        if self.domain not in self.schemas:
            self.schema = self.client.get(
                '{}{}swagger/?format=openapi'.
                format(self.domain, "/" if not self.
                       domain.endswith("/") else ""))
            self.schemas[self.domain] = self.schema
        else:
            self.schema = self.schemas[self.domain]

    def get_users(self):
        """
        This method returns the Resource that allows us manage the users in
        caravaggio

        :return: a Resource instance for UserResource
        """
        return UserResource(api=self)

    def get_organizations(self):
        """
        This method returns the Resource that allows us manage the
        organizations in caravaggio

        :return: a Resource instance for OrganizationResource
        """
        return OrganizationResource(api=self)
