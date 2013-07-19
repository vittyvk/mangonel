from basetest import BaseTest

from katello.client.server import ServerRequestError

from mangonel.environment import Environment
from mangonel.organization import Organization
from mangonel.system import System
from mangonel.systemgroup import SystemGroup
from mangonel.server import Server
from mangonel.user import User

import time
import unittest

class TestUsers(BaseTest):

    def setUp(self):
        BaseTest.setUp(self)

        self.server = Server(host=self.host,
                       project=self.project,
                       username=self.user,
                       password=self.password,
                       port=self.port)
        self.org_api = Organization()
        self.env_api = Environment()
        self.sys_api = System()
        self.sys_grp_api = SystemGroup()
        self.user_api = User()

        self.start_time = time.time()

    def tearDown(self):
        self.server = None

        self.ellapsed_time = time.time() - self.start_time
        self.logger.info("Test ellapsed time: %s" % self.ellapsed_time)

    def test_create_user_1(self):
        "Creates a new system user."

        user = self.user_api.create()
        self.assertEqual(user, self.user_api.user(user['id']))
