# -*- coding: utf-8 -*-
from collective.consent import log
from plone import api
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer


@implementer(INonInstallable)
class HiddenProfiles(object):
    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            'collective.consent:uninstall',
        ]


def create_consents_container(context):
    portal = api.portal.get()
    portal_types = portal.portal_types
    if 'consents' in portal.objectIds():
        return
    consents_id = portal_types.constructContent(
        'Consents Container',
        portal,
        'consents',
        title='Consents',
    )
    consents_container = portal[consents_id]
    consents_container.reindexObject()
    api.content.transition(obj=consents_container, transition='publish')
    consents_url = consents_container.absolute_url()
    log.info('Created Consents Containter at: {0}'.format(consents_url))


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.
    create_consents_container(context)


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
