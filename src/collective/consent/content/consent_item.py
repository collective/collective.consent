# -*- coding: utf-8 -*-
# from plone.app.textfield import RichText
# from plone.autoform import directives
from plone.dexterity.content import Item
# from plone.namedfile import field as namedfile
from plone.supermodel import model
# from plone.supermodel.directives import fieldset
# from z3c.form.browser.radio import RadioFieldWidget
from zope import schema
from zope.interface import implementer


# from collective.consent import _


class IConsentItem(model.Schema):
    """ Marker interface and Dexterity Python Schema for ConsentItem
    """

    button_text = schema.TextLine(
        title=u'Button Text',
        description=u'The Text on the consent button, '
                    u'to give the consent/acknowledgement',
        required=True,
        default=u'I give my consent',
        readonly=False,
    )

    target_roles = schema.Set(
        title=u'Target Roles',
        description=u'Which user roles should see the message?',
        value_type=schema.Choice(
            vocabulary=u'plone.app.vocabularies.Roles'
        ),
        default=set([
            'Editor',
            'Contributor',
        ]),
        required=True,
        readonly=False,
    )

    consent_update_period = schema.Int(
        title=u'Consent Update Period',
        description=u'The time in days, after the user has to renew there consent.',
        required=False,
        default=0,
        readonly=False,
    )


@implementer(IConsentItem)
class ConsentItem(Item):
    """
    """
