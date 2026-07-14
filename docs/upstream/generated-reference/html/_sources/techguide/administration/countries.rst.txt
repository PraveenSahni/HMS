.. _techguide-administration-countries:countries:

Countries
=========

Tryton comes with builtin functionalities for specific country related data like postal codes or subdivisions.

You can import them in the following way (first line for Vanilla Installation only):

.. code-block:: console

    $ cdexe
    $ trytond_import_countries -c /path/trytond.conf -d <database>
    $ trytond_import_postal_codes -c trytond.conf -d <database> <two_letter_country_code>

Further Reading:

https://docs.tryton.org/7.0/modules-country/setup.html
