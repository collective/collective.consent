# -*- coding: utf-8 -*-
from collective.consent import _
from plone.app import textfield
from plone.dexterity.content import Item
from plone.supermodel import model
from zope import schema
from zope.interface import implementer


class IConsentItem(model.Schema):
    """Marker interface and Dexterity Python Schema for ConsentItem"""

    # Make sure to import: plone.app.textfield
    text = textfield.RichText(
        title=_(
            "Text",
        ),
        description=_(
            "The full text of the consent item.",
        ),
        default="",
        required=False,
        readonly=False,
    )

    button_text = schema.TextLine(
        title=_(
            "Button Text",
        ),
        description=_(
            "The Text on the consent button, " "to give the consent/acknowledgement",
        ),
        required=True,
        default="I give my consent",
        readonly=False,
    )

    target_roles = schema.Set(
        title=_(
            "Target Roles",
        ),
        description=_(
            "Which user roles should see the message?",
        ),
        value_type=schema.Choice(
            vocabulary="plone.app.vocabularies.Roles",
        ),
        default=set(
            [
                "Editor",
                "Contributor",
            ]
        ),
        required=True,
        readonly=False,
    )

    consent_update_period = schema.Int(
        title=_(
            "Consent Update Period",
        ),
        description=_(
            "The time in days, after the user has to renew there consent.",
        ),
        required=False,
        default=0,
        readonly=False,
    )


@implementer(IConsentItem)
class ConsentItem(Item):
    """ """
