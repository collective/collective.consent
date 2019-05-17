# -*- coding: utf-8 -*-

from collective.consent.utilities import get_consent_container
# from collective.consent import _
from Products.Five.browser import BrowserView
from plone import api


class ConsentItemConsentsView(BrowserView):

    def __call__(self):
        reset = 'reset_consents' in self.request.form
        self.consents = self.get_consents()
        if reset:
            self.reset_consents(self.context.UID())
        return self.index()

    def get_consents(self):
        consent_container = get_consent_container()
        records = consent_container.search_consents(
            consent_item_uid=self.context.UID(),
            valid_only=False,
        )
        return records

    def reset_consents(self, consent_uid):
        consent_container = get_consent_container()
        consent_container.make_consents_invalid(consent_uid)

    @property
    def edit_perm(self):
        return api.user.has_permission(
            'Modify portal content',
            obj=self.context,
        )
