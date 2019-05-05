# -*- coding: utf-8 -*-

from collective.consent.utilities import get_consent_container
# from collective.consent import _
from Products.Five.browser import BrowserView


class ConsentItemConsentsView(BrowserView):

    def __call__(self):
        self.consents = self.get_consents()
        return self.index()

    def get_consents(self):
        consent_container = get_consent_container()
        records = consent_container.search_consents(
            consent_item_uid=self.context.UID(),
            valid_only=False,
        )
        return records
