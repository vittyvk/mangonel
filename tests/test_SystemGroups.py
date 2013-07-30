from basetest import BaseTest

from katello.client.server import ServerRequestError

from mangonel.contentview import ContentView
from mangonel.contentviewdefinition import ContentViewDefinition
from mangonel.environment import Environment
from mangonel.organization import Organization
from mangonel.system import System
from mangonel.systemgroup import SystemGroup
from mangonel.server import Server

import time
import unittest

class TestSystemGroups(BaseTest):

    def setUp(self):
        BaseTest.setUp(self)

        self.server = Server(host=self.host,
                       project=self.project,
                       username=self.user,
                       password=self.password,
                       port=self.port)
        self.org_api = Organization()
        self.cv_api = ContentView()
        self.cvd_api = ContentViewDefinition()
        self.env_api = Environment()
        self.sys_api = System()
        self.sys_grp_api = SystemGroup()

        self.start_time = time.time()


    def tearDown(self):
        self.server = None

        self.ellapsed_time = time.time() - self.start_time
        self.logger.info("Test ellapsed time: %s" % self.ellapsed_time)

    def _create_org_env(self):
        "Generic method to create a new organization and one environment"

        org = self.org_api.create()
        self.logger.debug("Created organization %s" % org['name'])
        self.assertEqual(org, self.org_api.organization(org['name']), 'Failed to create and retrieve org.')

        env = self.env_api.create(org, 'Dev', 'Library')
        self.logger.debug("Created environemt %s" % env['name'])
        self.assertEqual(env, self.env_api.environment_by_name(org['label'], 'Dev'))

        return (org, env)

    def test_create_group_1(self):
        "Creates an empty system group."

        (org, env) = self._create_org_env()

        grp = self.sys_grp_api.create(org)
        self.assertEqual(grp, self.sys_grp_api.system_group(org, grp['id']))
        self.logger.debug("Created system group '%s'" % grp['name'])

    def test_create_and_delete_system_group_1(self):
        "Creates an empty system group and deletes it."

        (org, env) = self._create_org_env()

        grp = self.sys_grp_api.create(org)
        self.assertEqual(grp, self.sys_grp_api.system_group(org, grp['id']))
        self.logger.debug("Created system group '%s'" % grp['name'])

        self.sys_grp_api.delete(org, grp['id'])
        self.assertRaises(ServerRequestError, lambda: self.sys_grp_api.system_group(org, grp['id']))
        self.logger.debug("Deleted system group '%s'" % grp['name'])

    def test_create_and_copy_system_group_1(self):
        "Creates system group and copies it."
        (org, env) = self._create_org_env()

        grp1 = self.sys_grp_api.create(org)
        self.assertEqual(grp1, self.sys_grp_api.system_group(org, grp1['id']))
        self.logger.debug("Created system group '%s'" % grp1['name'])

        grp2 = self.sys_grp_api.create(org)
        self.assertEqual(grp2, self.sys_grp_api.system_group(org, grp2['id']))
        self.logger.debug("Created system group '%s'" % grp2['name'])
        self.assertEqual(len(self.sys_grp_api.system_groups(org)), 2)


    def test_create_group_with_system_1(self):
        "Creates system group and adds a system to it."
        (org, env) = self._create_org_env()

        grp = self.sys_grp_api.create(org)
        self.assertEqual(grp, self.sys_grp_api.system_group(org, grp['id']))
        self.logger.debug("Created system group '%s'" % grp['name'])

        cvd = self.cvd_api.create(org, 'CVD1')
        self.logger.debug("Created Content View Definition CVD1")

        self.cvd_api.publish(org, cvd['id'], 'PublishedCVD1')
        pcvd = self.cv_api.content_views_by_label_name_or_id(org, name='PublishedCVD1')
        self.logger.debug("Published Content View PublishedCVD1")

        library = self.env_api.environment_by_name(org['label'], 'Library')

        sys1 = self.sys_api.create(org, library, view_id=pcvd['id'])
        self.logger.debug("Created system %s" % sys1['uuid'])
        self.assertEqual(sys1['uuid'], self.sys_api.system(sys1['uuid'])['uuid'])

        self.assertEqual(len(self.sys_grp_api.system_group_systems(org, grp['id'])), 0)
        self.logger.debug("System group '%s' is empty" % grp['name'])

        self.sys_grp_api.add_systems(org, grp['id'], [sys1['uuid'],])
        self.assertEqual(len(self.sys_grp_api.system_group_systems(org, grp['id'])), 1)
        self.logger.debug("System group '%s' is not empty" % grp['name'])


    def test_create_group_with_system_and_delete_1(self):
        "Creates system group and adds a system to it."
        (org, env) = self._create_org_env()

        library = self.env_api.environment_by_name(org['label'], 'Library')

        grp = self.sys_grp_api.create(org)
        self.assertEqual(grp, self.sys_grp_api.system_group(org, grp['id']))
        self.logger.debug("Created system group '%s'" % grp['name'])

        sys1 = self.sys_api.create(org, library)
        self.logger.debug("Created system %s" % sys1['uuid'])
        self.assertEqual(sys1['uuid'], self.sys_api.system(sys1['uuid'])['uuid'])
        self.assertEqual(len(self.sys_grp_api.system_group_systems(org, grp['id'])), 0)
        self.logger.debug("System group '%s' is empty" % grp['name'])

        self.sys_grp_api.add_systems(org, grp['id'], [sys1['uuid'],])
        self.assertEqual(len(self.sys_grp_api.system_group_systems(org, grp['id'])), 1)
        self.logger.debug("System group '%s' is not empty" % grp['name'])

        self.sys_grp_api.remove_systems(org, grp['id'], [sys1['uuid'],])
        self.assertEqual(len(self.sys_grp_api.system_group_systems(org, grp['id'])), 0)
        self.logger.debug("System group '%s' is empty" % grp['name'])


    def test_create_group_with_system_and_copy_1(self):
        "Creates system group, adds a system to it and copies it."
        (org, env) = self._create_org_env()

        library = self.env_api.environment_by_name(org['label'], 'Library')

        grp1 = self.sys_grp_api.create(org)
        self.assertEqual(grp1, self.sys_grp_api.system_group(org, grp1['id']))
        self.logger.debug("Created system group '%s'" % grp1['name'])

        sys1 = self.sys_api.create(org, library)
        self.logger.debug("Created system %s" % sys1['uuid'])
        self.assertEqual(sys1['uuid'], self.sys_api.system(sys1['uuid'])['uuid'])

        self.assertEqual(len(self.sys_grp_api.system_group_systems(org, grp1['id'])), 0)
        self.logger.debug("System group '%s' is empty" % grp1['name'])

        self.sys_grp_api.add_systems(org, grp1['id'], [sys1['uuid'],])
        self.assertEqual(len(self.sys_grp_api.system_group_systems(org, grp1['id'])), 1)
        self.logger.debug("System group '%s' is not empty" % grp1['name'])

        grp2 = self.sys_grp_api.copy(org, grp1['id'])
        self.assertEqual(grp2, self.sys_grp_api.system_group(org, grp2['id']))
        self.logger.debug("Created system group '%s'" % grp2['name'])
        self.assertEqual(len(self.sys_grp_api.system_groups(org)), 2)
        self.assertEqual(len(self.sys_grp_api.system_group_systems(org, grp2['id'])), 1)
        self.logger.debug("System group '%s' is not empty" % grp2['name'])
