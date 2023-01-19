# -*- coding: utf-8 -*-
from collective.consent import _
from collective.consent import log
from collective.consent.content.consent_item import IConsentItem
from collective.consent.utilities import get_consent_container
from datetime import datetime
from datetime import timedelta
from plone import api
from plone.app.layout.viewlets import ViewletBase
from zope.component import getMultiAdapter


class CheckConsentViewlet(ViewletBase):
    """ """

    @property
    def user(self):
        return api.user.get_current()

    def check_has_given_consents(self, items):
        if IConsentItem.providedBy(self.context):
            # Skip checks for ConsentItem it self ;)
            return True, None
        user_roles = api.user.get_roles()
        consent_container = get_consent_container()
        if not consent_container:
            return True, None
        user_id = self.user.id
        for item in items:
            item_obj = item.getObject()
            expires = None
            if item_obj.consent_update_period:
                expires = datetime.now() - timedelta(item_obj.consent_update_period)
            if not len(item_obj.target_roles & set(user_roles)):
                log.info(
                    f"target_roles [${item_obj.target_roles}] doesn't match [${user_roles}]."
                )
                return True, None
            record = consent_container.get_consent(
                item.UID, user_id, valid_only=True, expires=expires
            )
            if not record:
                return False, item
        return True, None

    def get_consent_items(self):
        consent_container = get_consent_container()
        consent_items = api.content.find(
            portal_type="Consent Item",
            context=consent_container,
            review_state=["published"],
        )
        return consent_items

    def render(self):
        consent_items = self.get_consent_items()
        self.has_given_consents, item = self.check_has_given_consents(consent_items)
        if self.has_given_consents:
            return ""
        else:
            context_state = getMultiAdapter(
                (self.context, self.request), name="plone_context_state"
            )
            came_from = context_state.current_base_url()
            log.info(
                f"User ${self.user.id} has, not given consent for ${item.getURL()}"
            )
            api.portal.show_message(
                message=_("Please read the text and give your consent below!"),
                request=self.request,
            )
            redirect_url = item.getURL() + "?came_from=" + came_from
            return self.request.response.redirect(redirect_url)
