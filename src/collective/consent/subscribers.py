# -*- coding: utf-8 -*-
from collective.consent import log
from collective.consent.utilities import get_consent_container


def delete_consents(obj, event):
    consents = get_consent_container()
    if not consents:
        return
    consents.delete_consents(obj.UID())
    log.info(
        'Deleted saved consents for {0} on ObjectRemovedEvent'.format(
            obj.absolute_url_path(),
        ),
    )
