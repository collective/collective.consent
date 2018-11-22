# -*- coding: utf-8 -*-
from collective.consent.testing import COLLECTIVE_CONSENT_FUNCTIONAL_TESTING
from collective.consent.testing import COLLECTIVE_CONSENT_INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


class ConsentUtilIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_CONSENT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.app = self.layer['app']
        self.request = self.app.REQUEST
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.consents = api.content.create(
            container=self.portal,
            type='Consents Container',
            id='consents',
        )
        self.consent1 = api.content.create(
            container=self.consents,
            type='Consent Item',
            id='consent1',
        )
        self.consent2 = api.content.create(
            container=self.consents,
            type='Consent Item',
            id='consent2',
        )

    def test_get_consent(self):
        self.consents.save_consent(
            self.consent1.UID(),
            TEST_USER_ID,
            u'john@example.com',
            u'John Doe',
        )
        record = self.consents.get_consent(
            self.consent1.UID(),
            TEST_USER_ID,
        )
        self.assertTrue(record)
        self.assertEqual(
            record['user_id'],
            TEST_USER_ID,
        )

    def test_no_result_in_get_consent(self):
        record = self.consents.get_consent(
            self.consent1.UID(),
            TEST_USER_ID,
        )
        self.assertFalse(record)

    def test_save_consent(self):
        self.consents.save_consent(
            self.consent1.UID(),
            TEST_USER_ID,
            u'john@example.com',
            u'John Doe',
        )
        record = self.consents.get_consent(
            self.consent1.UID(),
            TEST_USER_ID,
        )
        self.assertTrue(record)
        self.assertEqual(
            record['user_id'],
            TEST_USER_ID,
        )
        self.assertTrue(record['valid'])

    def test_search_consents(self):
        self.consents.save_consent(
            self.consent1.UID(),
            TEST_USER_ID,
            u'john@example.com',
            u'John Doe',
        )
        self.consents.save_consent(
            self.consent2.UID(),
            TEST_USER_ID,
            u'john@example.com',
            u'John Doe',
        )
        self.consents.save_consent(
            self.consent2.UID(),
            TEST_USER_ID + '_2',
            u'jane@example.com',
            u'Jane Doe',
        )
        # get all consents for user_id:
        results = self.consents.search_consents(
            user_id=TEST_USER_ID,
        )
        results_list = [r for r in results]
        self.assertTrue(list(results_list))
        self.assertTrue(len(list(results_list)) == 2)

    def test_no_results_in_search_consents(self):
        results = self.consents.search_consents(
            user_id=TEST_USER_ID,
        )
        results_list = [r for r in results]
        self.assertTrue(len(results_list) == 0)

    def test_make_consent_invalid(self):
        self.consents.save_consent(
            self.consent1.UID(),
            TEST_USER_ID,
            u'john@example.com',
            u'John Doe',
        )
        self.consents.save_consent(
            self.consent2.UID(),
            TEST_USER_ID,
            u'john@example.com',
            u'John Doe',
        )
        # get all consents for user_id:
        results = self.consents.search_consents(
            user_id=TEST_USER_ID,
        )
        results_list = [r for r in results]
        self.assertTrue(results_list)
        self.assertTrue(len(results_list) == 2)

        self.consents.make_consent_invalid(
            self.consent2.UID(),
            TEST_USER_ID,
        )
        # get valid and invalid consents:
        results = self.consents.search_consents(
            user_id=TEST_USER_ID,
        )
        results_list = [r for r in results]
        self.assertTrue(results_list)
        self.assertTrue(len(results_list) == 2)
        # get only valid consents:
        results = self.consents.search_consents(
            user_id=TEST_USER_ID,
            valid_only=True,
        )
        results_list = [r for r in results]
        self.assertTrue(results_list)
        self.assertTrue(len(results_list) == 1)
        self.assertTrue(results_list[0]['valid'])

    def test_delete_consents(self):
        self.consents.save_consent(
            self.consent1.UID(),
            TEST_USER_ID,
            u'john@example.com',
            u'John Doe',
        )
        self.consents.save_consent(
            self.consent1.UID(),
            TEST_USER_ID + '_1',
            u'jane@example.com',
            u'Jane Doe',
        )
        self.consents.save_consent(
            self.consent2.UID(),
            TEST_USER_ID,
            u'john@example.com',
            u'John Doe',
        )
        # get a consents for a consent item by consent_item_uid:
        results = self.consents.search_consents(
            consent_item_uid=self.consent1.UID(),
        )
        results_list = [r for r in results]
        self.assertTrue(results_list)
        self.assertTrue(len(results_list) == 2)

        self.consents.delete_consents(self.consent1.UID())
        # search for consents for the consent_item_uid:
        results = self.consents.search_consents(
            consent_item_uid=self.consent1.UID(),
        )
        results_list = [r for r in results]
        self.assertFalse(results_list)

        # search for other not effected consents:
        results = self.consents.search_consents(
            consent_item_uid=self.consent2.UID(),
        )
        results_list = [r for r in results]
        self.assertTrue(results_list)


class ConsentUtilFunctionalTest(unittest.TestCase):

    layer = COLLECTIVE_CONSENT_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
