from common import *

import datetime
import json
import requests
import sys
import time

try:
    from katello.client.api.provider import ProviderAPI
except ImportError, e:
    print "Please install Katello CLI package."
    sys.exit(-1)


class Provider():
    api = ProviderAPI()

    def create_provider(self, org, name=None, description='Built by API', ptype='Custom', url=None):

        if name is None:
            name = generate_name(8)

        return self.api.create(name, org['label'], description, ptype, url)


    def delete_provider(self, name):
        return self.api.delete(name)


    def provider(self, pId):
        return self.api.provider(pId)


    def providers_by_org(self, org):
        return self.api.providers_by_org(org['label'])


    def sync(self, pId):
        task = self.api.sync(pId)[0]

        while task['state'] != 'finished':
            print "Synchronizing..."
            task = self.api.last_sync_status(pId)

        return task
