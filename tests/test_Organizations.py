#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from basetest import BaseTest

from katello.client.server import ServerRequestError
from mangonel.common import generate_name

from mangonel.environment import Environment
from mangonel.organization import Organization
from mangonel.server import Server

import time
import unittest

class TestOrganizations(BaseTest):

    def setUp(self):
        BaseTest.setUp(self)

        self.server = Server(host=self.host,
                       project=self.project,
                       username=self.user,
                       password=self.password,
                       port=self.port)
        self.org_api = Organization()
        self.env_api = Environment()

        self.start_time = time.time()


    def tearDown(self):
        self.server = None

        self.ellapsed_time = time.time() - self.start_time
        self.logger.info("Test ellapsed time: %s" % self.ellapsed_time)

    def test_create_org1(self):
        "Creates a new organization."

        org = self.org_api.create()
        self.logger.debug("Created organization %s" % org['name'])
        self.assertEqual(org, self.org_api.organization(org['name']), 'Failed to create and retrieve org.')


    def test_create_org2(self):
        "Creates a new organization and then deletes it."

        org = self.org_api.create()
        self.logger.debug("Created organization %s" % org['name'])
        self.assertEqual(org, self.org_api.organization(org['name']), 'Failed to create and retrieve org.')

        self.logger.info("Deleting organization %s" % org['name'])
        self.org_api.delete(org['name'])
        self.assertRaises(ServerRequestError, lambda: self.org_api.organization(org['name']))


    def test_create_org3(self):
        "Creates a new organization with an initial environment."

        org = self.org_api.create()
        self.logger.debug("Created organization %s" % org['name'])
        self.assertEqual(org, self.org_api.organization(org['name']), 'Failed to create and retrieve org.')

        env = self.env_api.create(org, 'Dev', 'Library')
        self.logger.debug("Created environemt %s" % env['name'])
        self.assertEqual(env, self.env_api.environment_by_name(org['label'], 'Dev'))

    def test_create_org4(self):
        "Creates a new organization with several environments."

        org = self.org_api.create()
        self.logger.debug("Created organization %s" % org['name'])
        self.assertEqual(org, self.org_api.organization(org['name']), 'Failed to create and retrieve org.')

        env = self.env_api.create(org, 'Dev', 'Library')
        self.logger.debug("Created environemt %s" % env['name'])
        self.assertEqual(env, self.env_api.environment_by_name(org['label'], 'Dev'))

        env = self.env_api.create(org, 'Testing', 'Dev')
        self.logger.debug("Created environemt %s" % env['name'])
        self.assertEqual(env, self.env_api.environment_by_name(org['label'], 'Testing'))

        env = self.env_api.create(org, 'Release', 'Testing')
        self.logger.debug("Created environemt %s" % env['name'])
        self.assertEqual(env, self.env_api.environment_by_name(org['label'], 'Release'))

    def test_create_org5(self):
        "Org name and labels are unique across the server."

        org = self.org_api.create()
        self.logger.debug("Created organization %s" % org['name'])
        self.assertEqual(org, self.org_api.organization(org['name']), 'Failed to create and retrieve org.')
        self.assertRaises(ServerRequestError, lambda: self.org_api.create(name=org['name'], label=org['label']))
        self.assertRaises(ServerRequestError, lambda: self.org_api.create(name=org['name'], label=generate_name()))
        self.assertRaises(ServerRequestError, lambda: self.org_api.create(name=generate_name(), label=org['label']))

    def test_invalid_org_names(self):
        "These organization names are not valid."

        orgname = "org-invalid-%s" % generate_name(2)

        org_names = [
            " ",
            " " + generate_name(2),
            generate_name(2) + " ",
            generate_name(256),
            ]

        for name in org_names:
            self.assertRaises(ServerRequestError, lambda: self.org_api.create(name=name, label="label-%s" % generate_name(2)))

    def test_valid_org_names(self):
        "These organization names are valid."

        org_names = [
            "org-valid-%s" % generate_name(2),
            "org-valid.%s" % generate_name(2),
            "org-valid-%s@example.com" % generate_name(2),
            u"նոր օգտվող-%s" % generate_name(2),
            u"新用戶-%s" % generate_name(2),
            u"नए उपयोगकर्ता-%s" % generate_name(2),
            u"нового пользователя-%s" % generate_name(2),
            u"uusi käyttäjä-%s" % generate_name(2),
            u"νέος χρήστης-%s" % generate_name(2),
            generate_name(1,1),
            generate_name(255),
            "foo@!#$%^&*( ) %s" % generate_name(),
            "<blink>%s</blink>" % generate_name(),
            "bar+{}|\"?hi %s" % generate_name(),

            ]

        for name in org_names:
            org = self.org_api.create(name=name, label="label-%s" % generate_name(2))
            self.logger.debug("Created organization %s" % org['name'])
            self.assertEqual(org, self.org_api.organization(org['label']))

    def test_valid_org_labels(self):
        "These organization labels are valid."

        org_labels = [
            " ",
            None,
            "label-invalid-%s" % generate_name(2),
            generate_name(128),
            '_%s' % "label-invalid-%s" % generate_name(2),
            '%s_' % "label-invalid-%s" % generate_name(2),
            'label_%s' % "label-invalid-%s" % generate_name(2),
            ]

        for label in org_labels:
            org = self.org_api.create(name=generate_name(3), label=label)
            self.logger.debug("Created organization %s" % org['name'])
            self.assertEqual(org, self.org_api.organization(org['label']))

    def test_invalid_org_labels(self):
        "These organization labels are not valid."

        org_labels = [
            " " + "label-invalid-%s" % generate_name(2),
            "label-invalid-%s" % generate_name(2) + " ",
            generate_name(129),
            '<bold>%s</bold>' % "label-invalid-%s" % generate_name(2),
            ]

        for label in org_labels:
            self.assertRaises(ServerRequestError, lambda: self.org_api.create(name=generate_name(3), label=label))
