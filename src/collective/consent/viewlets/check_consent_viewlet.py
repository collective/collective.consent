# -*- coding: utf-8 -*-

from plone.app.layout.viewlets import ViewletBase


class CheckConsentViewlet(ViewletBase):

    def get_message(self):
        return u'My message'

    def render(self):
        self.message = self.get_message()
        return self.index()
