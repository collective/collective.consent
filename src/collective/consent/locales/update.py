# -*- coding: utf-8 -*-

import os
import pkg_resources
import subprocess


target_path = 'src/collective/consent/'
locale_path = target_path + 'locales/'
i18ndude = './bin/i18ndude'


def locale_folder_setup(domain=None):
    os.chdir(locale_path)
    languages = [d for d in os.listdir('.') if os.path.isdir(d)]
    for lang in languages:
        folder = os.listdir(lang)
        if 'LC_MESSAGES' in folder:
            continue
        else:
            lc_messages_path = lang + '/LC_MESSAGES/'
            os.mkdir(lc_messages_path)
            cmd = 'msginit --locale={0} --input={1}.pot --output={0}/LC_MESSAGES/{1}.po'.format(   # NOQA: E501
                        lang,
                        domain,
                    )
            subprocess.call(
                cmd,
                shell=True,
            )

    os.chdir('../../../../')


def _rebuild(domain=None):
    cmd = '{0} rebuild-pot --pot {1}/{2}.pot --create {2} {3}'.format(
        i18ndude,
        locale_path,
        domain,
        target_path,
    )
    subprocess.call(
        cmd,
        shell=True,
    )


def _sync(domain=None):
    cmd = '{0} sync --pot {1}/{2}.pot {1}*/LC_MESSAGES/{2}.po'.format(
        i18ndude,
        locale_path,
        domain,
    )
    subprocess.call(
        cmd,
        shell=True,
    )


def update_locale():
    package_name = 'collective.consent'
    os.chdir(pkg_resources.resource_filename(package_name, ''))
    os.chdir('../../../')

    locale_folder_setup(domain=package_name)
    _sync(domain=package_name)
    _rebuild(domain=package_name)

    # also build locales für domain: plone
    locale_folder_setup(domain='plone')
    _sync(domain='plone')
    _rebuild(domain='plone')
