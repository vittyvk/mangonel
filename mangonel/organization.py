from common import *

import datetime
import json
import requests
import sys
import time

try:
    from katello.client.api.organization import OrganizationAPI    
except ImportError, e:
    print "Please install Katello CLI package."
    sys.exit(-1)


class Organization():
    api = OrganizationAPI()
    
    def create_org(self, name=None):

        if name is None:
            name = generate_name(8)
            
        label = "label-%s" % name
        description = "Generated automatically."

        return self.api.create(name, label, description)

    
    def delete_org(self, name):
        return self.api.delete(name)

    
    def organization(self, name):
        return self.api.organization(name)


    def organizations(self):
        return self.api.organizations()
