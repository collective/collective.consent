# -*- coding: utf-8 -*-
from collective.consent import _
from plone.dexterity.content import Item
from plone.supermodel import model
from zope import schema
from zope.interface import implementer
from plone.app import textfield


class IConsentItem(model.Schema):
    """ Marker interface and Dexterity Python Schema for ConsentItem
    """
    # Make sure to import: plone.app.textfield
    text = textfield.RichText(
        title=_(
            u'Text',
        ),
        description=_(
            u'The full text of the consent item.',
        ),
        default=u'',
        required=False,
        readonly=False,
    )

    button_text = schema.TextLine(
        title=_(
            u'Button Text',
        ),
        description=_(
            u'The Text on the consent button, '
            u'to give the consent/acknowledgement',
        ),
        required=True,
        default=u'I give my consent',
        readonly=False,
    )

    target_roles = schema.Set(
        title=_(
            u'Target Roles',
        ),
        description=_(
            u'Which user roles should see the message?',
        ),
        value_type=schema.Choice(
            vocabulary=u'plone.app.vocabularies.Roles',
        ),
        default=set([
            'Editor',
            'Contributor',
        ]),
        required=True,
        readonly=False,
    )

    consent_update_period = schema.Int(
        title=_(
            u'Consent Update Period',
        ),
        description=_(
            u'The time in days, after the user has to renew there consent.',
        ),
        required=False,
        default=0,
        readonly=False,
    )


@implementer(IConsentItem)
class ConsentItem(Item):
    """
    """
