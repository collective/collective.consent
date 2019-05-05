# -*- coding: utf-8 -*-

from collective.consent import log
from collective.consent.utilities import get_consent_container
from plone import api
from plone.app.layout.viewlets import ViewletBase


class CheckConsentViewlet(ViewletBase):
    @property
    def has_given_consent(self):
        consent_container = get_consent_container()
        user = api.user.get_current()
        user_id = user.id
        return consent_container.has_given_consent(user_id)

    def check_has_given_consents(self, items):
        user_roles = api.user.get_roles()
        consent_container = get_consent_container()
        user = api.user.get_current()
        user_id = user.id
        for item in items:
            if not len(item.getObject().target_roles & set(user_roles)):
                log.info(u"target_roles doesn't match: {0}.".format(user_roles))
                return True, None
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
            came_from = self.request.HTTP_REFERER
            log.info('No consent for {0}'.format(item.getURL()))
            return self.request.response.redirect(
                item.getURL() + u'?came_from=' + came_from
            )
