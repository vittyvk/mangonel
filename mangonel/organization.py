from common import *

import datetime
import json
import requests
import sys
import time

try:
    from katello.client import server
    from katello.client.api.organization import OrganizationAPI
except ImportError, e:
    print "Please install Katello CLI package."
    sys.exit(-1)


class Organization():
    api = OrganizationAPI()

    def create(self, name=None):

        if name is None:
            name = generate_name(8)

        if label is None:
            label = "label-%s" % name

        if description is None:
            description = "Generated automatically."

        return self.api.create(name, label, description)


    def get_or_create_org(self, name=None, label=None, description=None):
        try:
            org = self.api.organization(label)
        except server.ServerRequestError, e:
            if e[1]['displayMessage'] != "Couldn't find organization '%s'" % label:
                raise(e)
            org = self.create_org(name, label, description)

        return org


    def delete(self, name):
        return self.api.delete(name)


    def organization(self, name):
        return self.api.organization(name)


    def organizations(self):
        return self.api.organizations()


    def pools(self, name):
        return self.api.pools(name)
