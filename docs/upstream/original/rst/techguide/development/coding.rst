.. _techguide-development-coding:coding:

Coding
------

The GNU Health Hospital Information System component uses the
`Tryton <https://www.tryton.org/>`__ framework, the programming
language used is `Python <https://python.org/>`__. The code is hosted on
`Codeberg <https://codeberg.org/gnuhealth>`__
and versioned using Git.

.. _techguide-development-coding:coding-obtaining_your_copy_of_the_code:

Obtaining Your Copy of the Code
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can get your copy of the latest code by doing an anonymous checkout:

.. code-block:: console


        $ git clone https://codeberg.org/gnuhealth/his.git

You can also `browse the code online <https://codeberg.org/gnuhealth/his>`__.

.. _techguide-development-coding:coding-coding_style:

Coding style
^^^^^^^^^^^^

The coding style should follow the Python best `practices <https://www.python.org/dev/peps/pep-0008/>`__.
and the Tryton `guidelines <https://www.tryton.org/develop/guidelines/code>`__

.. _techguide-development-coding:coding-branching:

Branching
^^^^^^^^^

For the HIS we use the following branches:

* **main**: Stable permanent branch, every merging devel and other branches to it implies an increase of the version number.
* **devel**: Permanent branch, used for develop the next major or minor release, created from main branch and merge main branch frequently by gitmerge4gh.el tool.
* **translate**: Permanent branch, used for receiving Weblate translations, created from devel branch and merged into devel branch, po-export woodpecker ci auto manage it at the moment.
* **po-backport**: Permanent branch, used for backport po files from devel branch to main branch, used by 'Update po files' feature of gnuhealth-control, po-backport woodpecker ci auto manage it at the moment.
* **ci-test**: Permanent branch, used to test woodpecker ci, **do not merge it to other branch**.
* **ci-test-output**: Permanent branch, used to test woodpecker ci, **do not merge it to other branch**.
* **wip-branch-description**: If you can not finish one atomic commit in a day, please open a branch named wip-branch-description stating the target branch and a description of your feature or bugfix.
  For example: Developing a DHIS2 module for upcoming version will take more time and commits.
  Instead of flooding the devel branch with commits we will work on a separate branch and do a pull request once we finished it.
  Probably we will also squash commits in the pull request to not flood the history either.
