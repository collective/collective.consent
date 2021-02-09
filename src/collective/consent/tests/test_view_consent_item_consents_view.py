# -*- coding: utf-8 -*-
from collective.consent.testing import COLLECTIVE_CONSENT_FUNCTIONAL_TESTING
from collective.consent.testing import COLLECTIVE_CONSENT_INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID, TEST_USER_NAME
from zope.component import getMultiAdapter
from zope.component.interfaces import ComponentLookupError

import unittest


class ViewsIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_CONSENT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        api.content.create(self.portal.consents, "Consent Item", "consent-item")
        api.content.create(self.portal, "Document", "front-page")

    def test_consent_item_consents_view_is_registered(self):
        view = getMultiAdapter(
            (self.portal.consents["consent-item"], self.portal.REQUEST),
            name="consent-item-consents-view",
        )
        self.assertTrue(view.__name__ == "consent-item-consents-view")
        # self.assertTrue(
        #     'Sample View' in view(),
        #     'Sample View is not found in consent-item-consents-view'
        # )

    def test_consent_item_consents_view_not_matching_interface(self):
        with self.assertRaises(ComponentLookupError):
            getMultiAdapter(
                (self.portal["front-page"], self.portal.REQUEST),
                name="consent-item-consents-view",
            )

    def test_consent_item_consents_view_only_for_editors(self):
        setRoles(self.portal, TEST_USER_ID, ["Member"])
        api.user.revoke_roles(
            username=TEST_USER_NAME,
            roles=["Owner"],
            obj=self.portal.consents["consent-item"],
        )
        self.assertFalse(
            api.user.has_permission(
                "View",
                username=TEST_USER_NAME,
                obj=self.portal.consents["consent-item"],
            )
        )


class ViewsFunctionalTest(unittest.TestCase):

    layer = COLLECTIVE_CONSENT_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
