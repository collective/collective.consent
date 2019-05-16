# -*- coding: utf-8 -*-
from collective.consent import log
from collective.consent.utilities import get_consent_container


def delete_consents(event):
    obj = event.object
    consents = get_consent_container()
    consents.delete_consents(obj.UID())
    log.info(
        'Deleted saved consents for {0} on ObjectRemovedEvent'.format(
            obj.absolute_url_path()
        )
    )
