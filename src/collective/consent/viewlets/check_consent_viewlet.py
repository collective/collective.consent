# -*- coding: utf-8 -*-

from collective.consent import log
from collective.consent.content.consent_item import IConsentItem
from collective.consent.utilities import get_consent_container
from datetime import datetime
from datetime import timedelta
from plone import api
from plone.app.layout.viewlets import ViewletBase
from zope.component import getMultiAdapter


class CheckConsentViewlet(ViewletBase):
    """
    """

    def check_has_given_consents(self, items):
        if IConsentItem.providedBy(self.context):
            # Skip checks for ConsentItem it self ;)
            return True, None
        user_roles = api.user.get_roles()
        consent_container = get_consent_container()
        if not consent_container:
            return True, None
        user = api.user.get_current()
        user_id = user.id
        for item in items:
            item_obj = item.getObject()
            expires = None
            if item_obj.consent_update_period:
                expires = datetime.now() - timedelta(
                    item_obj.consent_update_period,
                )
            if not len(item_obj.target_roles & set(user_roles)):
                log.info(u"target_roles doesn't match: {0}.".format(user_roles))
                return True, None
            record = consent_container.get_consent(
                item.UID,
                user_id,
                valid_only=True,
                expires=expires,
            )
            if not record:
                return False, item
        return True, None

    def get_consent_items(self):
        consent_container = get_consent_container()
        consent_items = api.content.find(
            portal_type=u'Consent Item',
            context=consent_container,
            review_state=['published'],
        )
        return consent_items

    def render(self):
        consent_items = self.get_consent_items()
        self.has_given_consents, item = self.check_has_given_consents(
            consent_items,
        )
        if self.has_given_consents:
            return ''
        else:
            context_state = getMultiAdapter(
                (self.context, self.request), name="plone_context_state"
            )
            came_from = context_state.current_base_url()
            log.info('No consent for {0}'.format(item.getURL()))
            redirect_url = item.getURL() + u'?came_from=' + came_from
            return self.request.response.redirect(redirect_url, )
