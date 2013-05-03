from common import *
import json
import requests
import sys
import time


class api(object):

    def __init__(self, host, username, password):
        self.host = host
        self.api = "%s/api" % self.host
        self.session = requests.Session()
        self.session.auth = (username, password)
        self.session.verify=False

    def get_org(self, org_name):
        result = None

        orgs = self.url_get("organizations")

        if orgs:
            org = [org for org in orgs if org['name'] == org_name]

            if org:
                result = org[0]

        return result

    def get_org_environments(self, org, env_name):
        result = None

        envs = self.url_get("organizations/%s/environments" % org['label'])

        if envs:
            env = [env for env in envs if env['name'] == env_name]

            if env:
                result = env[0]

        return result


    def add_system(self, org, env_name):
        result = None

        env = self.get_org_environments(org, env_name)
        system = generate_system()

        system['organization_id'] = org['label']
        system['environment_id'] = env['id']

        result = self.url_post("systems", system)

        return result


    def url_get(self, url, timing=True):
        result = None

        # Strip leading forward slashes
        if url.startswith("/"): url = url[1:]

        r = self.session.get("%s/%s" % (self.api, url))
        if r.status_code == 200:
            result = r.json()

        return result


    def url_post(self, url, payload, timing=True):
        result = None

        # Strip leading forward slashes
        if url.startswith("/"): url = url[1:]

        headers = {'content-type': 'application/json'}

        r = self.session.post("%s/%s" % (self.api, url),
                         data=json.dumps(payload),
                         headers=headers)

        import epdb; epdb.st()
        if r.status_code == 200:
            result = r.json()

        return result
