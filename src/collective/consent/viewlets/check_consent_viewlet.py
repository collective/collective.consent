# -*- coding: utf-8 -*-

from collective.consent import log
from collective.consent.utilities import get_consent_container
from plone import api
from plone.app.layout.viewlets import ViewletBase


class CheckConsentViewlet(ViewletBase):
    def check_has_given_consents(self, items):
        consent_container = get_consent_container()
        user = api.user.get_current()
        user_id = user.id
        for item in items:
            record = consent_container.get_consent(
                item.UID,
                user_id,
                valid_only=True,
            )
            if not record:
                return False, item
        return True, None

    def get_consent_items(self):
        consent_container = get_consent_container()
        consent_items = api.content.find(
            portal_type=u'Consent Item',
            context=consent_container,
        )
        return consent_items

    def render(self):
        consent_items = self.get_consent_items()
        self.has_given_consents, item = self.check_has_given_consents(
            consent_items,
        )
        if self.has_given_consents:
            return self.index()
        else:
            log.info('No consent for {0}'.format(item.gtURL()))
            return self.request.response.redirect(item.getURL())
