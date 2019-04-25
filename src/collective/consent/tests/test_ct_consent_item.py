# -*- coding: utf-8 -*-
from collective.consent.content.consent_item import IConsentItem  # NOQA E501
from collective.consent.testing import COLLECTIVE_CONSENT_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


class ConsentItemIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_CONSENT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            'Consents Container',
            self.portal,
            'consents_container',
            title='Parent container',
        )
        self.parent = self.portal[parent_id]

    def test_ct_consent_item_schema(self):
        fti = queryUtility(IDexterityFTI, name='Consent Item')
        schema = fti.lookupSchema()
        self.assertEqual(IConsentItem, schema)

    def test_ct_consent_item_fti(self):
        fti = queryUtility(IDexterityFTI, name='Consent Item')
        self.assertTrue(fti)

    def test_ct_consent_item_factory(self):
        fti = queryUtility(IDexterityFTI, name='Consent Item')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IConsentItem.providedBy(obj),
            u'IConsentItem not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_consent_item_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.parent,
            type='Consent Item',
            id='consent_item',
        )

        self.assertTrue(
            IConsentItem.providedBy(obj),
            u'IConsentItem not provided by {0}!'.format(
                obj.id,
            ),
        )

    def test_ct_consent_item_globally_not_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Consent Item')
        self.assertFalse(
            fti.global_allow,
            u'{0} is globally addable!'.format(fti.id)
        )
