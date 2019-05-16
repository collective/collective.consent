# -*- coding: utf-8 -*-
from collective.consent.testing import COLLECTIVE_CONSENT_FUNCTIONAL_TESTING
from collective.consent.testing import COLLECTIVE_CONSENT_INTEGRATION_TESTING
from datetime import datetime
from datetime import timedelta
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getMultiAdapter

import unittest


# from zope.component.interfaces import ComponentLookupError


class ConsentItemViewIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_CONSENT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        api.content.create(self.portal, 'Document', 'front-page')
        api.content.create(self.portal.consents, 'Consent Item', 'consent-item')

    def test_consent_item_view_is_registered(self):
        view = getMultiAdapter(
            (self.portal.consents['consent-item'], self.portal.REQUEST),
            name='view',
        )
        self.assertTrue(view.__name__ == 'view')

    def test_consent_item_view_check_has_not_given_consent(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager', 'Editor'])
        view = getMultiAdapter(
            (self.portal.consents['consent-item'], self.portal.REQUEST),
            name='view',
        )
        self.assertFalse(view.has_given_consent)

    def test_consent_item_view_check_has_not_given_consent_not_in_roles(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        view = getMultiAdapter(
            (self.portal.consents['consent-item'], self.portal.REQUEST),
            name='view',
        )
        self.assertTrue(view.has_given_consent)

    def test_consent_item_view_check_has_given_consent(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager', 'Editor'])
        view = getMultiAdapter(
            (self.portal.consents['consent-item'], self.portal.REQUEST),
            name='view',
        )
        self.portal.consents.save_consent(
            self.portal.consents['consent-item'].UID(),
            TEST_USER_ID,
            u'john@example.com',
            u'John Doe',
        )
        self.assertTrue(view.has_given_consent)

    def test_consent_item_view_check_has_given_invalid_consent(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager', 'Editor'])
        self.portal.consents.save_consent(
            self.portal.consents['consent-item'].UID(),
            TEST_USER_ID,
            u'john@example.com',
            u'John Doe',
        )
        self.portal.consents.make_consent_invalid(
            self.portal.consents['consent-item'].UID(),
            TEST_USER_ID,
        )
        view = getMultiAdapter(
            (self.portal.consents['consent-item'], self.portal.REQUEST),
            name='view',
        )
        self.assertFalse(view.has_given_consent)

    def test_consent_item_view_check_has_given_not_expired_consent(self):
        self.portal.consents['consent-item'].consent_update_period = 360
        setRoles(self.portal, TEST_USER_ID, ['Manager', 'Editor'])
        view = getMultiAdapter(
            (self.portal.consents['consent-item'], self.portal.REQUEST),
            name='view',
        )
        past1 = datetime.now() + timedelta(-90)
        self.portal.consents.save_consent(
            self.portal.consents['consent-item'].UID(),
            TEST_USER_ID,
            u'john@example.com',
            u'John Doe',
            timestamp=datetime(past1.year, past1.month, past1.day),
        )
        self.assertTrue(view.has_given_consent)

    def test_consent_item_view_check_has_given_but_expired_consent(self):
        self.portal.consents['consent-item'].consent_update_period = 30
        setRoles(self.portal, TEST_USER_ID, ['Manager', 'Editor'])
        view = getMultiAdapter(
            (self.portal.consents['consent-item'], self.portal.REQUEST),
            name='view',
        )
        past1 = datetime.now() + timedelta(-90)
        self.portal.consents.save_consent(
            self.portal.consents['consent-item'].UID(),
            TEST_USER_ID,
            u'john@example.com',
            u'John Doe',
            timestamp=datetime(past1.year, past1.month, past1.day),
        )
        self.assertFalse(view.has_given_consent)


class ConsentItemViewFunctionalTest(unittest.TestCase):

    layer = COLLECTIVE_CONSENT_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
