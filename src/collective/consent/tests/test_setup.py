# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.consent.testing import COLLECTIVE_CONSENT_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.CMFPlone.utils import get_installer

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.consent is properly installed."""

    layer = COLLECTIVE_CONSENT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])

    def test_product_installed(self):
        """Test if collective.consent is installed."""
        self.assertTrue(self.installer.is_product_installed("collective.consent"))

    def test_browserlayer(self):
        """Test that ICollectiveConsentLayer is registered."""
        from collective.consent.interfaces import ICollectiveConsentLayer
        from plone.browserlayer import utils

        self.assertIn(ICollectiveConsentLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_CONSENT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstall_product("collective.consent")
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if collective.consent is cleanly uninstalled."""
        self.assertFalse(self.installer.is_product_installed("collective.consent"))

    def test_browserlayer_removed(self):
        """Test that ICollectiveConsentLayer is removed."""
        from collective.consent.interfaces import ICollectiveConsentLayer
        from plone.browserlayer import utils

        self.assertNotIn(ICollectiveConsentLayer, utils.registered_layers())
