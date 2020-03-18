# -*- coding: utf-8 -*
# Copyright (c) 2019 BuildGroup Data Services Inc.
# All rights reserved.
# This software is proprietary and confidential and may not under
# any circumstances be used, copied, or distributed.
from caravaggio_python_bindings.exceptions import DoesNotExist, \
    MultipleObjectsReturned
from caravaggio_python_bindings.resource import Resource


class OrganizationResource(Resource):

    def get_organizations(self, params={}):
        return self.action(
            ['users', 'organization_list'],
            params=params)["results"]

    def get_organization(self, id):
        overrides = {"url": self.get_absolute_url("users/organization/{}/".format(id))
                     }

        return self.action(
            ['users', 'organization_read'], overrides=overrides)

    def create_organization(self, data):
        return self.action(
            ['users', 'organization_create'], params=data)

    def update_organization(self, id, data, partial_update=True):
        overrides = {
            "url": self.get_absolute_url("users/organization/{}/".format(id))
        }

        action = "organization_update" \
            if not partial_update else "organization_partial_update"

        return self.action(
            ['users', action],
            validate=(not partial_update),
            params=data,
            overrides=overrides)

    def delete_organization(self, id, force=False):
        """
        Remove the organization from the system. The organization can only be
        removed if it doesn't have members. In order to remove organizations
        that already has members we need to activate the flag `force`.

        :param id: the id of the organization to be deleted
        :param force: if we want to force the deletion removing the members
            of the different relationships.
        :return:
        """

        # Remove members of relations if needed
        if force:
            organization = self.get_organization(id)
            emails = []

            users_api = self.api.get_users_resource()

            # Administrators
            for admin_id in organization["administrators"]:
                emails.append(users_api.get_user(admin_id)["email"])
            if len(emails) > 0:
                self.remove_administrator(id, emails)

            # Members
            for member_id in organization["members"]:
                emails.append(users_api.get_user(member_id)["email"])
            if len(emails) > 0:
                self.remove_member(id, emails)

            # Restricted Members
            for restricted_member_id in organization["restricted_members"]:
                emails.append(
                    users_api.get_user(restricted_member_id)["email"])
            if len(emails) > 0:
                self.remove_restricted_member(id, emails)

        overrides = {
            "url": self.get_absolute_url("users/organization/{}/".format(id))
        }

        return self.action(
            ['users', 'organization_delete'], overrides=overrides)

    def add_member(self, organization, emails):
        """
        Add a user to the list of members of the organization
        :param organization: an organization object (dict) or the Id of the
            organization
        :param emails: the email of emails of users we want to add to the
            relation
        :return:
        """
        return self._add_to_org_relationship("member", organization, emails)

    def remove_member(self, organization, emails):
        """
        Add a user to the list of members of the organization
        :param organization: an organization object (dict) or the Id of the
            organization
        :param emails: the email of emails of users we want to add to the
            relation
        :return:
        """
        return self._remove_to_org_relationship("member", organization, emails)

    def add_administrator(self, organization, emails):
        """
        Add a user to the list of administrators of the organization
        :param organization: an organization object (dict) or the Id of the
            organization
        :param emails: the email of emails of users we want to add to the
            relation
        :return:
        """
        return self._add_to_org_relationship(
            "administrator", organization, emails)

    def remove_administrator(self, organization, emails):
        """
        Add a user to the list of administrators of the organization
        :param organization: an organization object (dict) or the Id of the
            organization
        :param emails: the email of emails of users we want to add to the
            relation
        :return:
        """
        return self._remove_to_org_relationship(
            "administrator", organization, emails)

    def add_restricted_member(self, organization, emails):
        """
        Add a user to the list of restricted members of the organization
        :param organization: an organization object (dict) or the Id of the
            organization
        :param emails: the email of emails of users we want to add to the
            relation
        :return:
        """
        return self._add_to_org_relationship(
            "restricted_member", organization, emails)

    def remove_restricted_member(self, organization, emails):
        """
        Add a user to the list of restricted members of the organization
        :param organization: an organization object (dict) or the Id of the
            organization
        :param emails: the email of emails of users we want to add to the
            relation
        :return:
        """
        return self._remove_to_org_relationship(
            "restricted_member", organization, emails)

    def _add_to_org_relationship(self, relation, organization, emails):
        """
        Add a user to the relation list of the organization
        :param relation: the relation in which we want to add the user.
            Options: member, administrator, restricted_member
        :param organization: an organization object (dict) or the Id of the
            organization
        :param emails: the email of emails of users we want to add to the
            relation
        :return:
        """
        if isinstance(organization, dict):
            organization = organization["id"]

        overrides = {
            "url": self.get_absolute_url("users/organization/{}/add_{}/".format(organization, relation))
        }

        if not isinstance(emails, (list, set)):
            emails = [emails]

        params = {
            "users": emails
        }

        return self.action(
            ['users', 'organization_add_{}'.format(relation)],
            params=params,
            validate=False,
            overrides=overrides)

    def _remove_to_org_relationship(self, relation, organization, emails):
        """
        Remove a user to the relation list of the organization
        :param relation: the relation in which we want to remove the user.
            Options: member, administrator, restricted_member
        :param organization: an organization object (dict) or the Id of the
            organization
        :param emails: the email of emails of users we want to remove to the
            relation
        :return:
        """
        if isinstance(organization, dict):
            organization = organization["id"]

        overrides = {
            "url": self.get_absolute_url("users/organization/{}/remove_{}/".format(organization, relation))
        }

        if not isinstance(emails, (list, set)):
            emails = [emails]

        params = {
            "users": emails
        }

        return self.action(
            ['users', 'organization_remove_{}'.format(relation)],
            params=params,
            validate=False,
            overrides=overrides)


class UserResource(Resource):

    def get_user_token(self, email):
        data = {
            "email": email
        }

        return self.action(
            ['admin-token-auth', 'create'],
            params=data,
            validate=False)["token"]

    def get_user(self, id):
        overrides = {
            "url": self.get_absolute_url("users/user/{}/".format(id))}
        return self.action(
            ['users', 'user_read'], overrides=overrides)

    def get_users(self, params={}):
        return self.action(
            ['users', 'user_list'], params=params)

    def get_user_by_email(self, email):
        params = {
            "email": email
        }

        results = self.action(
            ['users', 'user_list'], params=params)

        if results["count"] == 0:
            raise DoesNotExist(
                "There is no user  with the informed email [{}]".format(email))
        elif results["count"] > 1:
            raise MultipleObjectsReturned(
                "Multiple users found with the same email [{}]".format(email))

        return results["results"][0]

    def create_user(self, data):
        return self.action(
            ['users', 'user_create'], params=data)

    def update_user(self, id, data, partial_update=True):
        overrides = {
            "url": self.get_absolute_url("users/user/{}/".format(id))}

        action = "user_update" if not partial_update else "user_partial_update"
        return self.action(
            ['users', action],
            validate=(not partial_update),
            params=data,
            overrides=overrides)

    def delete_user(self, id):
        overrides = {
            "url": self.get_absolute_url("users/user/{}/".format(id))}

        return self.action(
            ['users', 'user_delete'], overrides=overrides)
