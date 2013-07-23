from basetest import BaseTest

from katello.client.server import ServerRequestError
from mangonel.common import generate_name

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

    def test_create_user_2(self):
        "Creates a new system user with specific arguments."

        username = "user-%s" % generate_name(4)
        userpass = generate_name(8)
        useremail = "%s@example.com" % username

        user = self.user_api.create(username, userpass, useremail)
        self.assertEqual(user['username'], username)
        self.assertEqual(user['email'], useremail)

    def test_create_user_3(self):
        "Username validation"

        username = "user-%s" % generate_name(4)

        self.assertRaises(ServerRequestError, lambda: self.user_api.create(name=' '))
        self.assertRaises(ServerRequestError, lambda: self.user_api.create(name=' ' + username))
        self.assertRaises(ServerRequestError, lambda: self.user_api.create(name=username + ' '))
        self.assertRaises(ServerRequestError, lambda: self.user_api.create(name='aa'))
        self.assertRaises(ServerRequestError, lambda: self.user_api.create(name='<bold>%s</bold>' % username))
        self.assertRaises(ServerRequestError, lambda: self.user_api.create(name='a'*129))

    def test_create_user_4(self):
        "Empty username is not allowed"

        self.assertRaises(ServerRequestError, lambda: self.user_api.create(name=' '))

    def test_update_user_email_and_succeed_1(self):
        "Creates and updates a system user's email."

        user = self.user_api.create()
        self.assertEqual(user, self.user_api.user(user['id']))

        self.user_api.update(user['id'], **{'email': 'changed@example.com'})
        user = self.user_api.user(user['id'])
        self.assertEqual(user['email'], 'changed@example.com')

    def test_update_user_email_and_fail_1(self):
        "Creates and updates a system user's email."

        user = self.user_api.create()
        self.assertEqual(user, self.user_api.user(user['id']))

        self.assertRaises(ServerRequestError, lambda: self.user_api.update(user['id'], **{'email': ' '}))

        # Nothing should have changed
        self.assertEqual(user, self.user_api.user(user['id']))

    def test_delete_user_1(self):
        "Creates and deletes a system user."

        user = self.user_api.create()
        self.assertEqual(user, self.user_api.user(user['id']))

        self.user_api.delete(user['id'])
        self.assertRaises(ServerRequestError, lambda: self.user_api.user(user['id']))
