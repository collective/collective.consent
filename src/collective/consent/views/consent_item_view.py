# -*- coding: utf-8 -*-

# from collective.consent import _
from collective.consent import log
from collective.consent.utilities import get_consent_container
from plone import api
# from Products.Five.browser import BrowserView
from plone.dexterity.browser.view import DefaultView


# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class ConsentItemView(DefaultView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('consent_item_view.pt')

    def __call__(self):
        self.user_info = self.get_user_info()
        consent_uid = self.request.form.get('consent_uid')
        if consent_uid:
            user_id = self.request.form.get('user_id')
            submit_value = self.request.form.get('submit')
            self.save_consent(consent_uid, user_id, submit_value)
        self.has_given_consent = self.check_has_given_consent()
        return super(ConsentItemView, self).__call__()

    def save_consent(self, consent_uid, user_id, submit_value):
        if user_id != self.user_info['id']:
            log.error(
                u'Current user id differs from form user id,'
                u' cancel save_consent!',
            )
            return
        consent_container = get_consent_container()
        consent_container.save_consent(
            consent_uid,
            user_id,
            self.user_info['email'],
            self.user_info['fullname'],
        )

    def get_user_info(self):
        user_info = dict()
        user = api.user.get_current()
        user_info['id'] = user.id
        user_info['email'] = user.getProperty('email')
        user_info['fullname'] = user.getProperty('fullname')
        user_info['edit_perm'] = api.user.has_permission(
            'Modify portal content',
            obj=self.context,
        )
        return user_info

    def check_has_given_consent(self):
        consent_container = get_consent_container()
        record = consent_container.get_consent(
            self.context.UID,
            self.user_info['id'],
            valid_only=True,
        )
        if not record:
            return False
        return True
