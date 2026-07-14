.. _techguide-localization-index:localization:

Localization
============

Translations are stored module-wise in .po files located in directories called *locale*.
Trytons builtin features are described here:

https://docs.tryton.org/7.0/server/topics/translation.html

However we use Weblate to manage the translation:

https://weblate.org/en/

.. _techguide-localization-index:localization-translating_gnu_health:

Translating GNU Health
----------------------

The language of the GNU Health user interface is controlled through gettext language packs.

Language packs are are managed, stored and distributed through an online translation platform. This makes maintaining translations easier and faster, and it makes your GNU Health installation leaner, since it contains only the languages needed by your health institution.

The official GNU Health translation portal is now hosted at `Weblate <https://hosted.weblate.org/projects/gnu-health/>`_.

There is a mailing list for all translation related discussions at https://lists.gnu.org/mailman/listinfo/health-i18n . If you are a GNU Health translator, you should subscribe to this mailing list.

When translating GNU Health to your language, please start from the *health* module which contains the core of GNU Health.

.. _techguide-localization-index:localization-installation_of_language_packs:

Installation of Language Packs
------------------------------
We will go through an example on how to enable the Spanish language and to install the language pack. For this example, we will work on the demo database :code:`gnuhealth_demo_generic`.

* **Step 1:** Declare your language and make it translatable. This can be done in the *Administration → Localization → Languages* section.

Remember the code of the language (in this case **es**).

* **Step 2:** Download and uncompress the language pack file.

With the GNU Health administrator user (*gnuhealth*) execute the following commands.

.. note::
    Substitute the language sample code (es) by your language

.. warning::
    The language files come from po-backport branch of HIS git: https://codeberg.org/gnuhealth/his/archive/po-backport.tar.gz , the official version and languages are shipped in the standard installation. Always try in a development environment before use in production. This will overwrites the existing translation files! **User should use gnuhealth-control tool in devel branch** .

.. code-block:: console


    $ ghcontrol.py -> Update po file menu


This installs *all the modules* translation files for the Spanish Spain (es) language.

* **Step 3:** Change your user preferences to your new language:
* **Step 4:** Log out and stop your GNU Health Tryton server (if it's running).
* **Step 5:** Update your GNU Health instance with the command

.. code-block:: console


    $ trytond-admin --all --database=gnuhealth_demo_generic


Sometime, the about command may not work well as expected, user can try below way:

1. Open language form: Administration > Localization > Languages > <YOUR-LANG>
2. Click 'Unload translations' then click 'Load translations'", the below script can simplify this steps.

   .. code-block:: console

      $ python his-utils/scripts/upgrade-utils/5.0/reload-languages.py -h


* **Step 6:** Start your sever with the new language for your module installed.

.. _techguide-localization-index:localization-setting_the_user_language:

Setting the User Language
-------------------------

Please remember that the language is a user preference. In the same database, you can have different users using different languages.
Read the :ref:`userguide-healthcenter-accessmanagement:access_management-users-preferences_tab` chapter to see how.



.. _techguide-localization-index:localization-update_po_and_pot_files:

Update po and pot files
-----------------------

**NOTE: This section is mainly used by GNU Health HIS developers.**

GNU Health have a tool named *po-export* in scripts directory of
his-utils repo, it can be used to update po and pot files, it support
two modes:

.. code-block:: console

   $ cd his-utils/scripts/po-export
   $ bash po-export.sh --his-dir <your-his-repo> --lang 'zh_CN fr'

The languages with :code:`--lang` argument will be exported with the
buildin function of tryton directly, it run slower but get better
fuzzy match, the rest will be handled by gettext msgmerge command and
do not use fuzzy match, if adding new language which is not exist in
health locale directory, suggest use :code:`--new-lang` instead.

Using :code:`--fast-export` will greatly accelerate export speed by
skip some modules with huge xml data file.

When HIS code is updated, for example: labels and helps of fields,
report templates or data files, developer can **install new version of
gnuhealth git**, then run *po-export.sh* to update pot and po files,
if use just want to test, try below command:

.. code-block:: console

   $ bash po-export.sh --fast-export --his-dir <your-his-repo> --pot

.. Note::

    Frequently installing of gnuhealth git is a very troublesome
    thing, we can use devel-installer in his-utils, which will link
    his git repo to trytond/modules directory, it is more convenient
    but only applicable to the development environment.

    .. code-block:: console

       $ bash his-utils/devel-installer/devel-installer.sh -h


Before run *po-export.sh*, the following steps is suggested, for they
can reduce po files merge conflicts.

1. Open GNU Health weblate page: (https://translate.codeberg.org/projects/gnuhealth)
2. Lock translation: *(Manage > Repository maintenance > Lock)*
3. Commit pending changes: *(Manage > Repository maintenance > (pending changes) Commit)*
4. Push outgoing commits: *(Manage > Repository maintenance > Push)*
5. Pull and update changes from gnuhealth upstream repo to your working repo.

After run *po-export.sh* successfully:

1. Push po files changes to GNU Health upstream repo.
2. Open GNU Health weblate page: (https://translate.codeberg.org/projects/gnuhealth)
3. Sync all changes to weblate: *(Manage > Repository maintenance > (missing commits) Update)*
4. Unlock translation: *(Manage > Repository maintenance > Unlock)*
