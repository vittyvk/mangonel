from common import *

import datetime
import json
import sys
import time

try:
    from katello.client.api.repo import RepoAPI
except ImportError, e:
    print "Please install Katello CLI package."
    sys.exit(-1)


class Repository(RepoAPI):

    def __init__(self):
        super(Repository, self).__init__()

    def create(self, org, prd, url, name=None, label=None, unprotected=True, gpgkey=None, nogpgkey=None):

        if name is None:
            name = generate_name(8)

        if label is None:
            label = "label-%s" % name.lower()

        return super(Repository, self).create(org['label'], prd['id'], name, label, url, unprotected, gpgkey, nogpgkey)

    def repositories_by_product(self, org, prd, includeDisabled=False):
        return super(Repository, self).repositories_by_repo(org['label'], prd['id'], includeDisabled)
