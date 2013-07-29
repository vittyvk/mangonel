from common import *

import sys

try:
    from katello.client.api.environment import EnvironmentAPI
except ImportError, e:
    print "Please install Katello CLI package."
    sys.exit(-1)


class Environment(EnvironmentAPI):

    def __init__(self):
        super(Environment, self).__init__()

    def create(self, org, name=None, prior='Library', label=None, description=None):

        if name is None:
            name = generate_name()

        if prior:
            prior = self.environment_by_name(org['label'], prior)
            prior_id = prior['id']

        return super(Environment, self).create(org['label'], name, label, description, prior_id)
