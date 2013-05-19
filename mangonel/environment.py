from common import *

import sys

try:
    from katello.client.api.environment import EnvironmentAPI
except ImportError, e:
    print "Please install Katello CLI package."
    sys.exit(-1)


class Environment():
    api = EnvironmentAPI()
    
    def create_environment(self, org, name=None, prior='Library'):

        if name is None:
            name = generate_name()

        if prior:
            prior = self.environment_by_name(org, prior)
            prior_id = prior['id']
            
        label = "label-%s" % name.replace(' ', '_')
        description = "Generated automatically."

        return self.api.create(org['label'], name, label, description, prior_id)


    def environment_by_name(self, org, name):
        return self.api.environment_by_name(org['label'], name)
