import logging
import logging.config

import os
import unittest


class BaseTest(unittest.TestCase):

    def setUp(self):
        self.host = os.getenv('HOST')
        self.project = os.getenv('PROJECT', None)
        self.user = os.getenv('USERNAME', None)
        self.password = os.getenv('PASSWORD', None)
        self.port = os.getenv('PORT', None)

        logging.config.fileConfig("logging.conf")

        self.logger = logging.getLogger("mangonel")
