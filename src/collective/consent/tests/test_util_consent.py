# -*- coding: utf-8 -*-
# from collective.consent.testing import COLLECTIVE_CONSENT_FUNCTIONAL_TESTING
from collective.consent.testing import COLLECTIVE_CONSENT_INTEGRATION_TESTING
from datetime import datetime
from datetime import timedelta
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
        self.consents = self.portal.consents
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
        self.consents.save_consent(
            self.consent1.UID(),
            TEST_USER_ID + 'b',
            u'john@example.com',
            u'John Doe b',
            valid=False,
        )
        record1 = self.consents.get_consent(
            self.consent1.UID(),
            TEST_USER_ID,
        )
        self.assertTrue(record1)
        self.assertEqual(
            record1['user_id'],
            TEST_USER_ID,
        )

        # make sur we dont't get an invalid record
        record2 = self.consents.get_consent(
            self.consent1.UID(),
            TEST_USER_ID + 'b',
            valid_only=True,
        )
        self.assertFalse(record2)

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

        # make sure that old records of the same consent/user are removed:
        self.consents.save_consent(
            self.consent1.UID(),
            TEST_USER_ID,
            u'john@example.com',
            u'John Doe',
        )
        results = self.consents.search_consents(
            consent_item_uid=self.consent1.UID(),
            user_id=TEST_USER_ID,
        )
        self.assertTrue(len(list(results)) == 1)

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
        results = self.consents.search_consents(user_id=TEST_USER_ID, )
        results_list = [r for r in results]
        self.assertTrue(list(results_list))
        self.assertTrue(len(list(results_list)) == 2)

    def test_no_results_in_search_consents(self):
        results = self.consents.search_consents(user_id=TEST_USER_ID, )
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
        results = self.consents.search_consents(user_id=TEST_USER_ID, )
        results_list = [r for r in results]
        self.assertTrue(results_list)
        self.assertTrue(len(results_list) == 2)

        self.consents.make_consent_invalid(
            self.consent2.UID(),
            TEST_USER_ID,
        )
        # get valid and invalid consents:
        results = self.consents.search_consents(user_id=TEST_USER_ID, )
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

    def test_make_consents_invalid(self):
        self.consents.save_consent(
            self.consent1.UID(),
            TEST_USER_ID,
            u'john@example.com',
            u'John Doe',
        )
        self.consents.save_consent(
            self.consent1.UID(),
            TEST_USER_ID + '_b',
            u'john@example.com',
            u'John Doe',
        )
        # get all consents for user_id:
        results = self.consents.search_consents(
            consent_item_uid=self.consent1.UID(),
        )
        results_list = [r for r in results]
        self.assertTrue(results_list)
        self.assertTrue(len(results_list) == 2)

        self.consents.make_consents_invalid(self.consent1.UID(), )
        # get valid and invalid consents:
        results = self.consents.search_consents(
            consent_item_uid=self.consent1.UID(),
        )
        results_list = [r for r in results]
        self.assertTrue(results_list)
        self.assertTrue(len(results_list) == 2)

        # get only valid consents:
        results = self.consents.search_consents(
            consent_item_uid=self.consent1.UID(),
            valid_only=True,
        )
        results_list = [r for r in results]
        self.assertFalse(results_list)
        self.assertTrue(len(results_list) == 0)

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

    def test_search_unexpired_consents(self):
        today = datetime.today()
        self.consent1.consent_update_period = 80
        self.consent2.consent_update_period = 360
        past1 = today + timedelta(-90)
        self.consents.save_consent(
            self.consent1.UID(),
            TEST_USER_ID,
            u'john@example.com',
            u'John Doe',
            timestamp=datetime(past1.year, past1.month, past1.day),
        )
        past2 = today + timedelta(-90)
        self.consents.save_consent(
            self.consent2.UID(),
            TEST_USER_ID,
            u'jane@example.com',
            u'Jane Doe',
            timestamp=datetime(past2.year, past2.month, past2.day),
        )
        # get all consents for user_id / consent_item_uid:
        results = self.consents.search_consents(
            consent_item_uid=self.consent2.UID(),
            user_id=TEST_USER_ID,
        )
        results_list = [r for r in results]
        self.assertTrue(list(results_list))
        self.assertTrue(len(list(results_list)) == 1)

        # get all consents for user_id / consent_item_uid not older than update period:
        results = self.consents.search_consents(
            consent_item_uid=self.consent1.UID(),
            user_id=TEST_USER_ID,
            expires=today + timedelta(-self.consent1.consent_update_period),
        )
        results_list = [r for r in results]
        self.assertFalse(list(results_list))

        # get all consents for user_id / consent_item_uid not older than update period:
        results = self.consents.search_consents(
            consent_item_uid=self.consent2.UID(),
            user_id=TEST_USER_ID,
            expires=today + timedelta(-self.consent2.consent_update_period),
        )
        results_list = [r for r in results]
        self.assertTrue(list(results_list))
        self.assertTrue(len(list(results_list)) == 1)

#
# class ConsentUtilFunctionalTest(unittest.TestCase):
#
#     layer = COLLECTIVE_CONSENT_FUNCTIONAL_TESTING
#
#     def setUp(self):
#         self.portal = self.layer['portal']
#         setRoles(self.portal, TEST_USER_ID, ['Manager'])
