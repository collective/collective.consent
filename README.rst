==================
collective.consent
==================

.. note:: THIS IS STILL IN PROGRESS!

Provides a functionality to ask users for consent to different topics, before they can continue. One can add multiple consent items and define which user will have to give there consent based on there permission roles. Each of this users have to give the consent before they can continue to work.

This is realized by viewlet which will check a list of consents for each user/consent_item combination and redirect the user to the consent item case they still have to give there consent.

Internally the consents are stored in a soup on the ConsentsContainer object.

Features
--------

- Allows you to add multiple consent items (documents).
- A consent item consists of a Title, Description, RichText and a custom button text.
- Also you can define an update period, where the user has to give the consent again.
- For every consent item one can choose the target permissions roles.
- One can reset (invalidate) all existing consents for a consent item.


Installation
------------

Install collective.consent by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.consent


and then running ``bin/buildout``, start Plone and activate the add-on in the add-on's control panel. Then add a ConsentContainer on the top-level (portal-root).

Contributors
------------

- Maik Derstappen (MrTango) - md@derio.de


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.consent/issues
- Source Code: https://github.com/collective/collective.consent


Support
-------

If you are having issues, please let us know.


License
-------

The project is licensed under the GPLv2.
