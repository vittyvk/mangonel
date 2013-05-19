from common import *

import datetime
import json
import requests
import sys
import time

try:
    from katello.client.api.system import SystemAPI
except ImportError, e:
    print "Please install Katello CLI package."
    sys.exit(-1)


class System():
    api = SystemAPI()
    
    def create_system(self, name=None):

        if name is None:
            name = generate_name(8)
            
        label = "label-%s" % name
        description = "Generated automatically."

        return self.api.register(name, org, env, activationkey, cp_type, facts)
