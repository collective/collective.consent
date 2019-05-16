# -*- coding: utf-8 -*-
# from collective.consent.viewlets.check_consent_viewlet import CheckConsentViewlet
from collective.consent.interfaces import ICollectiveConsentLayer
# from collective.consent.testing import COLLECTIVE_CONSENT_FUNCTIONAL_TESTING
from collective.consent.testing import COLLECTIVE_CONSENT_INTEGRATION_TESTING
from datetime import datetime
from datetime import timedelta
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.Five.browser import BrowserView as View
from zope.component import queryMultiAdapter
from zope.interface import alsoProvides
from zope.viewlet.interfaces import IViewletManager

import unittest


class ViewletIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_CONSENT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.app = self.layer['app']
        self.request = self.app.REQUEST
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        api.content.create(self.portal, 'Document', 'other-document')
        api.content.create(self.portal.consents, 'Consent Item', 'consent-item')
        api.content.transition(
            obj=self.portal.consents['consent-item'], transition='publish'
        )

    def get_check_consent_viewlet(self, context):
        view = View(context, self.request)
        manager_name = 'plone.abovecontenttitle'
        alsoProvides(self.request, ICollectiveConsentLayer)
        manager = queryMultiAdapter(
            (context, self.request, view),
            IViewletManager,
            manager_name,
            default=None
        )
        manager.update()
        my_viewlet = [
            v for v in manager.viewlets if v.__name__ == 'check-consent-viewlet'
        ]
        return my_viewlet[0]

    def test_check_consent_viewlet_is_registered(self):
        view = View(self.portal['other-document'], self.request)
        manager_name = 'plone.abovecontenttitle'
        alsoProvides(self.request, ICollectiveConsentLayer)
        manager = queryMultiAdapter(
            (self.portal['other-document'], self.request, view),
            IViewletManager,
            manager_name,
            default=None
        )
        self.assertIsNotNone(manager)
        manager.update()
        my_viewlet = [
            v for v in manager.viewlets if v.__name__ == 'check-consent-viewlet'
        ]
        self.assertEqual(len(my_viewlet), 1)

    def test_check_consent_viewlet_has_given_consent(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager', 'Editor'])
        self.portal.consents['consent-item'].consent_update_period = 0
        past1 = datetime.now() + timedelta(-90)
        self.portal.consents.save_consent(
            self.portal.consents['consent-item'].UID(),
            TEST_USER_ID,
            u'john@example.com',
            u'John Doe',
            timestamp=datetime(past1.year, past1.month, past1.day),
        )
        viewlet = self.get_check_consent_viewlet(self.portal['other-document'])
        consent_items = viewlet.get_consent_items()
        has_given_consents, item = viewlet.check_has_given_consents(
            consent_items,
        )
        self.assertTrue(has_given_consents)

    def test_check_consent_viewlet_has_given_but_expired_consent(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager', 'Editor'])
        self.portal.consents['consent-item'].consent_update_period = 30
        past1 = datetime.now() + timedelta(-90)
        self.portal.consents.save_consent(
            self.portal.consents['consent-item'].UID(),
            TEST_USER_ID,
            u'john@example.com',
            u'John Doe',
            timestamp=datetime(past1.year, past1.month, past1.day),
        )
        viewlet = self.get_check_consent_viewlet(self.portal['other-document'])
        consent_items = viewlet.get_consent_items()
        has_given_consents, item = viewlet.check_has_given_consents(
            consent_items,
        )
        self.assertFalse(has_given_consents)


# class ViewletFunctionalTest(unittest.TestCase):
#
#     layer = COLLECTIVE_CONSENT_FUNCTIONAL_TESTING
#
#     def setUp(self):
#         self.portal = self.layer['portal']
#         setRoles(self.portal, TEST_USER_ID, ['Manager'])
#
