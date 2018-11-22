from repoze.catalog.catalog import Catalog
from repoze.catalog.indexes.field import CatalogFieldIndex
from souper.interfaces import ICatalogFactory
from souper.soup import get_soup
from souper.soup import NodeAttributeIndexer
from zope.interface import implementer
from zope.interface import Interface
from zope.site.hooks import getSite


@implementer(ICatalogFactory)
class ConsentCatalogFactory(object):

    def __call__(self, context=None):
        catalog = Catalog()
        catalog[u'consent_id'] = CatalogFieldIndex(
            NodeAttributeIndexer('consent_id')
        )
        catalog[u'consent_item_uid'] = CatalogFieldIndex(
            NodeAttributeIndexer('consent_item_uid')
        )
        catalog[u'user_id'] = CatalogFieldIndex(
            NodeAttributeIndexer('user_id')
        )
        catalog[u'user_email'] = CatalogFieldIndex(
            NodeAttributeIndexer('user_email')
        )
        catalog[u'user_fullname'] = CatalogFieldIndex(
            NodeAttributeIndexer('user_fullname')
        )
        catalog[u'timestamp'] = CatalogFieldIndex(
            NodeAttributeIndexer('timestamp')
        )
        catalog[u'valid'] = CatalogFieldIndex(
            NodeAttributeIndexer('valid')
        )
        return catalog
