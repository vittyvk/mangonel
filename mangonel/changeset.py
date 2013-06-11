from common import *

import datetime
import json
import requests
import sys
import time

try:
    from katello.client.api.task_status import TaskStatusAPI
    from katello.client.api.changeset import ChangesetAPI    
except ImportError, e:
    print "Please install Katello CLI package."
    sys.exit(-1)


class Changeset():
    task_api = TaskStatusAPI()
    api = ChangesetAPI()

    def create(self, org, env, name=None, type_in='promotion', description=None):

        if name is None:
            name = generate_name(8)

        if description is None:
            description = "Promoted on %s" % datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

        return self.api.create(name, org['label'], env['id'], type_in, description)


    def delete(self, chsId):
        return self.api.delete(chsId)

    
    def changeset(self, chsId):
        return self.api.changeset(chsId)


    def changeset_by_name(self, org, env, name):
        return self.api.changeset_by_name(org['label'], env['id'], name)


    def add_content(self, chsId, content, contentType='content_views'):
        return self.api.add_content(chsId, contentType, {'content_view' : content['id'] })

    def apply(self, chsId):
        applyTask = self.api.apply(chsId)

        task = self.task_api.status(applyTask['uuid'])
        while task['state'] != 'finished':
            self.logger.debug("Promoting content...")
            task = self.task_api.status(applyTask['uuid'])

