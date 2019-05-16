# -*- coding: utf-8 -*-
from collective.consent.content.consents_container import IConsentsContainer  # NOQA E501
from collective.consent.testing import COLLECTIVE_CONSENT_INTEGRATION_TESTING  # noqa
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


class ConsentsContainerIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_CONSENT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_ct_consents_container_schema(self):
        fti = queryUtility(IDexterityFTI, name='Consents Container')
        schema = fti.lookupSchema()
        self.assertEqual(IConsentsContainer, schema)

    def test_ct_consents_container_fti(self):
        fti = queryUtility(IDexterityFTI, name='Consents Container')
        self.assertTrue(fti)

    def test_ct_consents_container_factory(self):
        fti = queryUtility(IDexterityFTI, name='Consents Container')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IConsentsContainer.providedBy(obj),
            u'IConsentsContainer not provided by {0}!'.format(obj, ),
        )

    def test_ct_consents_container_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        portal_types = self.portal.portal_types
        portal_types['Consents Container'].global_allow = True
        obj = api.content.create(
            container=self.portal,
            type='Consents Container',
            id='consents_container',
        )

        self.assertTrue(
            IConsentsContainer.providedBy(obj),
            u'IConsentsContainer not provided by {0}!'.format(obj.id, ),
        )

    def test_ct_consents_container_filter_content_type_true(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Consents Container')
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            'consents_container_id',
            title='Consents Container container',
        )
        self.parent = self.portal[parent_id]
        with self.assertRaises(InvalidParameterError):
            api.content.create(
                container=self.parent,
                type='Document',
                title='My Content',
            )
