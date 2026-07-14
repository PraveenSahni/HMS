.. _techguide-demodb:local_demo_database:

Local Demo Database
-------------------

If you want to have demo data but save your modifications, access without internet, etc. then you can get a local demo database.

Switch to the gnuhealth user and use the installer script. You can get it from his-utils tools: https://codeberg.org/gnuhealth/his-utils .

.. code-block:: console
        :substitutions:


        $ his-utils/scripts/demodb/install_demo_database.sh |version_nodot|

This will download the demo database of version |version|. It will also create the database locally.

Now enter the database name in the GNU Health client. For example, for |version| releases:

* **Database:** health50
* **Username:** admin
* **Password:** gnusolidario

There is a user "admin_es" that uses the Spanish language.

You can browse the current demo databases from our download area:

https://www.gnuhealth.org/downloads/postgres_dumps/

.. hint::

        Remember that **databases with odd minor numbers (eg, 41) are unstable**. They are the development version of the upcoming release, and for dev / testing purposes.
