# -*- coding: utf-8 -*-

# from collective.consent import _
from collective.consent import log
from collective.consent.utilities import get_consent_container
from datetime import datetime
from datetime import timedelta
from plone import api
# from Products.Five.browser import BrowserView
from plone.dexterity.browser.view import DefaultView


# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class ConsentItemView(DefaultView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('consent_item_view.pt')

    def __call__(self):
        consent_button_text = self.request.form.get('consent_button_text')
        submit = 'submit' in self.request.form
        reset = 'reset_consents' in self.request.form
        consent_uid = self.request.form.get('consent_uid')
        user_id = self.request.form.get('user_id')
        self.came_from = self.request.form.get('came_from')
        if submit:
            self.save_consent(consent_uid, user_id, consent_button_text)
            return self.request.response.redirect(self.came_from)
        if reset:
            self.reset_consents(consent_uid)
        return super(ConsentItemView, self).__call__()

    def reset_consents(self, consent_uid):
        consent_container = get_consent_container()
        consent_container.make_consents_invalid(consent_uid)

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

    @property
    def user_info(self):
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

    @property
    def has_given_consent(self):
        user_roles = api.user.get_roles()
        if not len(self.context.target_roles & set(user_roles)):
            log.info(u"target_roles doesn't match: {0}.".format(user_roles))
            return True
        consent_container = get_consent_container()
        expires = None
        if self.context.consent_update_period:
            expires = datetime.now() - timedelta(
                self.context.consent_update_period,
            )
        record = consent_container.get_consent(
            self.context.UID(),
            self.user_info['id'],
            valid_only=True,
            expires=expires,
        )
        if not record:
            return False
        return True
