.. _techguide-contributing:contributing:

Contributing
============
.. _techguide-contributing:contributing-contributors_wanted!:

Contributors Wanted!
--------------------

GNU Health is a :abbr:`FLOSS (Free/Libre/Open-Source Software)` project, you are very welcome to contribute to it. There are several ways to do so, most of which not requiring you to know how to code!

If you want to join developing please check :ref:`techguide-development-index:development_environment`.

.. _techguide-contributing:contributing-translating_the_software:

Translating the Software
------------------------

Providing GNU Health in a user's native language is a big part of the success. You can help by improving existing translations, or creating a new translation in your own language. Translating GNU Health is easy, it does not require technical knowledge, and is all done via a web interface. Have a look at the :ref:`techguide-localization-index:localization` page for more details on the process.

.. _techguide-contributing:contributing-writing_the_documentation:

Writing the Documentation
-------------------------

Maintaining the documentation is a complex task and support is always welcome!
The GNU Health documentation was migrated from Wikibooks to our new Git repository on Codeberg where Sphinx is used to write it.

If you just want to do minor changes you can edit the source inside Codeberg in the browser:

https://codeberg.org/gnuhealth/documentation/src/branch/test

After committing or having a pull request accepted you can view the results here after some seconds:

https://gnuhealth.codeberg.page/testpages/

For bigger changes it is recommended to get a local copy like this (on Debian):

.. code-block:: console

        $ sudo apt install git pipx
        $ pipx ensurepath
        $ source ~/.bashrc
        $ git clone https://codeberg.org/gnuhealth/documentation.git
        $ cd documentation/his
        $ pipx install sphinx
        $ pipx runpip sphinx install -r requirements.txt
        $ make html

Afterwards you can double click health-doc/build/index.html from file browser to open it in internet browser and see your local working copy.
If you already have developer access don't forget to clone using SSH instead of HTTPS.

After making changes you should not just run ``make html`` but use the script ``docbuild.sh`` inside ``documentation/his``. It first calls the Python script ``label.py`` which ensures that label names are consitent, then removes the last build and then finally runs the build. Additionally it is linting the repository.
Besides it already contains a case differentiation for FreeBSD where you would run ``gmake html``.

There are some guidelines for this documentation:

* Don't use hard coded version numbers for GNU Health or the Tryton version.
  Those are defined in ``source/conf.py`` and have to be updated after a version increase.
* Image files are stored in ``source/images/``
* For screenshots we use the ``thumbnails`` directive.
  We set the title, but do not set *show_caption* to true.
  We use PNG files <= 500 KB. The appearance themes should not differ too much from the ones
  in the existing screenshots.
  If applicable you should see in the menu on the left how you opened the view in the center.
  For annotations we use red rectangles with a line width of 3 or 4 pixels.
* In shell code snippets we use the ``console`` style because it allows to double-click the command
  without getting the $ or # sign into your copy. We use # for root and $ for non root commands.
  Note that styles like ``ini``, ``sql`` or ``pycon`` should also be used if applicable.
  Sphinx uses ``pygments`` which supports numereous languages: https://pygments.org/languages/
* Lines should not have more than 80 characters
* Don't commit if the commands inside ``docbuild.sh`` throw errors.
* Check all modified pages locally before committing.
* From time to time run the shell script ``detect_broken_links.sh`` to find outdated links.

.. _techguide-contributing:contributing-reporting_bugs:

Reporting Bugs
--------------

Unfortunately almost any software contains bugs. While we are actively working on fixing them so you don't have to struggle, please do report any bug or anomaly that you encounter.

Reporting a bug does not take much time. It is done via `Savannah <https://savannah.gnu.org/bugs/?group=health>`__.

Tip: For faster resolution, please include a description of the steps you performed to get to the bug, and if possible include screenshots of the issue. But be careful: '''Don't include patient information in the screenshots or your description!'''

.. _techguide-contributing:contributing-coding:


.. _techguide-contributing:contributing-coding-customizing_and_creating_your_own_modules:


.. _techguide-contributing:contributing-reporting_bugs-submitting_patches:

Submitting Patches
^^^^^^^^^^^^^^^^^^

Regular contributors have write access to the code repository. However, if you're just starting out, we want to make sure that your changes get reviewed. The way to do this is to `open a bug <https://savannah.gnu.org/bugs/?group=health>`_ describing the issue you've fixed or the feature you've added, and to attach a patch to that bug report. One of the developers will review your patch and commit it to the main development branch if approved.
