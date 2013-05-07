from common import *
import json
import requests
import sys
import time


class api(object):

    def __init__(self, host, project='katello', username='admin', password='admin'):
        """
        Initiates a session to the provided host, using credentials.
        """

        # Some clean up
        if not host.startswith("https://"):
            if not host.startswith("http://"):
                host = "https://%s" % host
            else:
                host = "https://%s" % host[7:]
                
        if host.endswith("/"):
            host = "%s%s" % (host, project)
        else:
            host = "%s/%s" % (host, project)

        self.host = host
        self.api = "%s/api" % self.host
        self.session = requests.Session()
        self.session.auth = (username, password)
        self.session.verify=False



    def get_env_by_name(self, org, name):

        result = None

        environments = self.url_get("organizations/%s/environments" % org['label'])

        if environments:
            env = [env for env in environments if env['label'] == name]

        if env:
            result = env[0]

        return result

    
    def create_env(self, org, name=None, prior='Library'):

        env = None
        
        if name is None:
            name = generate_name()

        prior_env = self.get_env_by_name(org, prior)

        if prior:
            env = {'environment':
                       {'name': name, 'prior': prior_env['id']}}

            env = self.url_post("organizations/%s/environments" % org['label'], env)

        return env

    
    def create_org(self, org=None):
 
        if org is None:
            name = generate_name(8)
            org = {
                'name': name,
                'label': "label-%s" % name,
                'description': "Generated automatically.",}

        org = self.url_post("organizations", org)

        return org


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


    def get_systems(self, org):
        """
        Returns a list of all systems that belong to an organization.
        """

        result = []
        
        systems = self.url_get("organizations/%s/systems" % org['label'])

        if systems:
            result = systems.json()

        return result


    def get_system_by_name(self, org, name):
        """
        Returns a system from an organization.
        """

        result = None

        system = [system for system in self.get_systems(org) if system['name'] == name]

        if system:
            result = system[0]

        return result


    def create_system(self, org, env_name):
        result = None

        env = self.get_org_environments(org, env_name)
        system = generate_system()

        system['organization_id'] = org['label']
        system['environment_id'] = env['id']

        result = self.url_post("systems", system)

        return result


    def delete_system(self, org, system_name):

        system = self.get_system_by_name(org, system_name)

        if system:
            status = self.url_delete("systems/%s" % system['uuid'])


    def url_get(self, url, timing=60):
        """
        Performs a GET using the url provided and waits (default) for
        60 seconds before timing out.
        """
        result = None

        # Strip leading forward slashes
        if url.startswith("/"): url = url[1:]

        try:
            r = self.session.get("%s/%s" % (self.api, url), timeout=timing)
            if r.status_code == 200:
                result = r.json()
            else:
                print "Failed to GET url '%s': %s" % (url, r.text)
        except requests.exceptions.Timeout, e:
            print "Your request has timed out."
            pass

        return result


    def url_post(self, url, payload, timing=60):
        """
        Performs a POST using the url provided and waits (default) for
        60 seconds before timing out.
        """
        result = None

        # Strip leading forward slashes
        if url.startswith("/"): url = url[1:]

        headers = {'content-type': 'application/json'}

        try:
            r = self.session.post("%s/%s" % (self.api, url),
                                  data=json.dumps(payload),
                                  headers=headers,
                                  timeout=timing)
            if r.status_code == 200:
                result = r.json()
            else:
                print "Failed to POST to url '%s': %s" % (url, r.text)

        except requests.exceptions.Timeout, e:
            print "Your request has timed out."
            pass

        return result


    def url_delete(self, url, timing=60):
        """
        Performs a GET using the url provided and waits (default) for
        60 seconds before timing out.
        """
        result = False

        # Strip leading forward slashes
        if url.startswith("/"): url = url[1:]

        try:
            r = self.session.delete("%s/%s" % (self.api, url), timeout=timing)
            if r.status_code == 204:
                result = True
            else:
                print "Failed to DELETE: %s" % r.text
        except requests.exceptions.Timeout, e:
            print "Your request has timed out."
            pass

        return result
