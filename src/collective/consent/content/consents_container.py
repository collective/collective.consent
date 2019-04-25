# -*- coding: utf-8 -*-
from datetime import datetime
# from plone import api
from plone.dexterity.content import Container
from plone.supermodel import model
from repoze.catalog.query import And
from repoze.catalog.query import Eq
from souper.plone.interfaces import ISoupRoot
from souper.soup import get_soup
from souper.soup import Record
from zope.interface import implementer


# from collective.consent import _


class IConsentsContainer(model.Schema):
    """ Marker interface and Dexterity Python Schema for ConsentsContainer
    """


@implementer(IConsentsContainer, ISoupRoot)
class ConsentsContainer(Container):
    """
    """

    # def __init__(self, id=None, **kwargs):
    #     super(ConsentsContainer, self).__init__(id, **kwargs)

    # @property
    # def portal(self):
    #     return api.portal.get()

    @property
    def consents_soup(self):
        soup = get_soup('collective_consent_consents', self)
        return soup

    def save_consent(
        self,
        consent_item_uid,
        user_id,
        user_email,
        user_fullname,
    ):
        """ Save a consent of a given user_id for the given consent item
        """
        record = Record()
        record.attrs['consent_id'] = u'{0}:{1}'.format(
            consent_item_uid,
            user_id,
        )
        record.attrs['consent_item_uid'] = consent_item_uid
        record.attrs['user_id'] = user_id
        record.attrs['email'] = user_email
        record.attrs['fullname'] = user_fullname
        record.attrs['valid'] = True
        record.attrs['timestamp'] = datetime.now()
        rec_id = self.consents_soup.add(record)
        return rec_id

    def search_consents(
        self,
        consent_item_uid=None,
        user_id=None,
        valid_only=False,
    ):
        """ Returns a list of consent items.
            If no consent entry was found, it returns an empty list.
        """
        queries = []
        if valid_only:
            queries.append(Eq('valid', True))
        if consent_item_uid:
            queries.append(Eq('consent_item_uid', consent_item_uid))
        if user_id:
            queries.append(Eq('user_id', user_id))
        if not queries:
            []
        records = (r.attrs for r in self.consents_soup.query(And(*queries)))
        return records

    def get_consent(self, consent_item_uid, user_id, valid_only=False):
        """ Returns a consent entry of a given user_id for a given
            consent_item. If no consent entry exists, return None
        """
        record = None
        records = self.search_consents(
            consent_item_uid=consent_item_uid,
            user_id=user_id,
            valid_only=valid_only,
        )
        try:
            record = records.next()
        except StopIteration:
            pass
        return record

    def delete_consents(self, consent_item_uid):
        """ Delete all consents for the given consent_item_uid.
            Useful for event handler when a consent item is deleted.
        """
        query = Eq('consent_item_uid', consent_item_uid)
        records = self.consents_soup.query(query)
        for record in records:
            del self.consents_soup[record]
        # self.consents_soup.reindex(records=records)

    def make_consent_invalid(self, consent_item_uid, user_id):
        """ Find the consent for a given consent_item_uid and user_id and
            set valid=False
        """
        query = And(
            Eq('consent_item_uid', consent_item_uid),
            Eq('user_id', user_id),
        )
        records = [r for r in self.consents_soup.query(query)]
        if not records:
            return
        records[0].attrs['valid'] = False
        self.consents_soup.reindex(records=[records[0]])
