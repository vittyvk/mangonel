from basetest import BaseTest

from katello.client.server import ServerRequestError

class TestActivationKeys(BaseTest):

    def test_get_ak_1(self):
        "Tries to fetch an invalid activationkey."

        org = self.org_api.create()
        self.logger.debug("Created organization %s" % org['name'])
        self.assertEqual(org, self.org_api.organization(org['name']), 'Failed to create and retrieve org.')

        self.assertRaises(ServerRequestError, lambda: self.ak_api.activation_key(org, 10000))

    def test_create_ak_1(self):
        "Assures that a content view is passed during creation."

        org = self.org_api.create()
        self.logger.debug("Created organization %s" % org['name'])
        self.assertEqual(org, self.org_api.organization(org['name']), 'Failed to create and retrieve org.')

        env1 = self.env_api.create(org, 'Dev', 'Library')
        self.logger.debug("Created environemt %s" % env1['name'])
        self.assertEqual(env1, self.env_api.environment_by_name(org['label'], 'Dev'))

        self.assertRaises(ServerRequestError, lambda: self.ak_api.create(env1))

    def test_create_ak_2(self):
        "Creates a new activationkey against default content view."

        org = self.org_api.create()
        self.logger.debug("Created organization %s" % org['name'])
        self.assertEqual(org, self.org_api.organization(org['name']), 'Failed to create and retrieve org.')

        env1 = self.env_api.create(org, 'Dev', 'Library')
        self.logger.debug("Created environemt %s" % env1['name'])
        self.assertEqual(env1, self.env_api.environment_by_name(org['label'], 'Dev'))

        pcvd = self.cv_api.content_views_by_label_name_or_id(org, name='Default Organization View')

        library = self.env_api.environment_by_name(org['label'], 'Library')

        ak1 = self.ak_api.create(library, cvId=pcvd['id'])
        self.logger.debug("Created activationkey %s" % ak1['name'])
        self.assertEqual(ak1, self.ak_api.activation_key(org, ak1['id']))

    def test_create_ak_3(self):
        "Creates a new activationkey with no content."

        org = self.org_api.create()
        self.logger.debug("Created organization %s" % org['name'])
        self.assertEqual(org, self.org_api.organization(org['name']), 'Failed to create and retrieve org.')

        env1 = self.env_api.create(org, 'Dev', 'Library')
        self.logger.debug("Created environemt %s" % env1['name'])
        self.assertEqual(env1, self.env_api.environment_by_name(org['label'], 'Dev'))

        cvd = self.cvd_api.create(org, 'CVD1')
        self.logger.debug("Created Content View Definition CVD1")

        self.cvd_api.publish(org, cvd['id'], 'PublishedCVD1')
        pcvd = self.cv_api.content_views_by_label_name_or_id(org, name='PublishedCVD1')
        library = self.env_api.environment_by_name(org['label'], 'Library')

        ak1 = self.ak_api.create(library, cvId=pcvd['id'])
        self.logger.debug("Created activationkey %s" % ak1['name'])
        self.assertEqual(ak1, self.ak_api.activation_key(org, ak1['id']))

    def test_create_ak_4(self):
        "Creates a new activationkey and adds a pool."

        org = self.org_api.create()
        self.logger.debug("Created organization %s" % org['name'])
        self.assertEqual(org, self.org_api.organization(org['name']), 'Failed to create and retrieve org.')

        env1 = self.env_api.create(org, 'Dev', 'Library')
        self.logger.debug("Created environemt %s" % env1['name'])
        self.assertEqual(env1, self.env_api.environment_by_name(org['label'], 'Dev'))

        cvd = self.cvd_api.create(org, 'CVD1')
        self.logger.debug("Created Content View Definition CVD1")

        self.cvd_api.publish(org, cvd['id'], 'PublishedCVD1')
        pcvd = self.cv_api.content_views_by_label_name_or_id(org, name='PublishedCVD1')
        self.logger.debug("Published Content View PublishedCVD1")

        library = self.env_api.environment_by_name(org['label'], 'Library')

        ak1 = self.ak_api.create(library, cvId=pcvd['id'])
        self.logger.debug("Created activationkey %s" % ak1['name'])
        self.assertEqual(ak1, self.ak_api.activation_key(org, ak1['id']))

        prv = self.prv_api.create(org, 'Provider1')
        self.logger.debug("Created custom provider Provider1")
        self.assertEqual(prv, self.prv_api.provider(prv['id']))

        prd = self.prd_api.create(prv, 'Product1')
        self.logger.debug("Created product Product1")
        self.assertEqual(prd['id'], self.prd_api.product(org, prd['id'])['id'])

        repo = self.repo_api.create(org, prd, 'http://hhovsepy.fedorapeople.org/fakerepos/zoo4/', 'Repo1')
        self.logger.debug("Created repositiry Repo1")
        self.assertEqual(repo, self.repo_api.repo(repo['id']))

        # Sync
        self.prv_api.sync(prv['id'])
        self.assertEqual(self.prv_api.provider(prv['id'])['sync_state'], 'finished')
        self.logger.debug("Finished synchronizing Provider1")

        #TODO: There seems to be a delay between sync and pools being available
        pools = self.org_api.pools(org['label'])

        for pool in pools:
            self.ak_api.add_pool(org, ak1['id'], pool['id'])
            self.assertTrue(self.ak_api.has_pool(org, ak1['id'], pool['id']))
            self.logger.debug("Added pool id '%s'' to activationkey '%s'" % (pool['id'], ak1['name']))
