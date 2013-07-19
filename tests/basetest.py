import logging
import logging.config

import os
import unittest


class BaseTest(unittest.TestCase):

    def setUp(self):
        self.host = os.getenv('KATELLO_HOST')
        self.port = os.getenv('KATELLO_PORT', '443')
        self.project = os.getenv('PROJECT', '/katello')

        # Make sure that PROJECT starts with a leading "/"
        if not self.project.startswith("/"): self.project = "/" + self.project

        self.user = os.getenv('KATELLO_USERNAME', None)
        self.password = os.getenv('KATELLO_PASSWORD', None)
        self.verbosity = int(os.getenv('VERBOSITY', 3))

        logging.config.fileConfig("logging.conf")

        self.logger = logging.getLogger("mangonel")
        self.logger.setLevel(self.verbosity * 10)
