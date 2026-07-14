.. _techguide-administration-upgrade:upgrade:

Upgrade
=======
.. _techguide-administration-upgrade:upgrade-about_gnu_health_upgrades:

About GNU Health Upgrades
-------------------------

GNU Health is in constant development. Upgrades fix bugs and keep your system with the latest functionality. Therefore, you are advised to keep your production system with the latest version.

GNU Health will always provide the scripts and tools for you to keep your health center updated.

.. _techguide-administration-upgrade:upgrade-upgrade_vs_updates:

Upgrade vs updates
------------------

We define *upgrade* as the process of adapting an existing database instance and GNU Health kernel to a new version (eg, 4.4 -> 5.0), that usually involves refactoring and change in the database schema. Upgrade is a major process
that requirees planning ahead of time. It's a project by itself.

When we talk about *update* is the process of patching a current kernel and / or the depending libraries. These type of operation is now done by :ref:`techguide-administration-controlcenter:the_gnu_health_control_center` and is, most of the time, an automated process.

In both cases, **always** make a backup of your production database.

This chapter refers to the *upgrade* process.

.. _techguide-administration-upgrade:upgrade-gathering_information:

Gathering Information
---------------------

**Get the latest GNU Health versions and announces**: A key point to keep your GNU Health environment in good shape is to become part of the community. We publish GNU Health version updates and other relevant news in different media. Make sure you subscribe at least to the General users and to the health announce mailing lists.

**Verify your current GNU Health version**: You can check your current GNU Health database version from the client, via *Administration → Modules*.


**Always upgrade all the GNU Health modules**: When we release a version, we always pack all the official modules on it. This is important, because we test the integrity and cross-functionality among modules. So, **you should never use modules from different versions**. For example, you should not use :code:`health_genetics` version 4.4.0 with :code:`health` 4.6 . This is not supported and can create serious inconsistencies on your database!

.. _techguide-administration-upgrade:upgrade-prepare_your_upgrade:

Prepare your Upgrade
--------------------

**Plan your upgrade process, resources and downtime**: Upgrading a hospital information system requires careful planning. Make sure you choose the right time, and notice your colleagues about the new release.

**Test the upgrade process in another computer**: It is highly recommended that you count with a separate server, where you can test your upgrade process in a controlled environment, without impacting your production installation. Write down all the steps and issues that you run into.

.. _techguide-administration-upgrade:upgrade-the_upgrade_process:

The Upgrade Process
-------------------

This section summarizes the upgrade process steps for a standard installation, using the modules included in the official release at GNU.org FTP site. Any version specific information will sent via the '''health-announce@gnu.org''' mailing list, along the new release announcement, so make sure you are subscribed!

.. important::
        Backup the database, attachments and kernel (modules)

**Step 1:** Stop your Tryton server.

**Step 2:** Backup your database and GNU Health directories

If you are still in version 4.4, the following lines will make a backup of your DB in your
home directory ad then copy the whole $HOME to an external device or wherever you decide.


.. code-block:: console

        $ cd $HOME
        $ pg_dump your_db > your_db_backup.sql
        $ cp -a $HOME /your/backup/destination_directory


.. note::
    GNU Health 5.0 onwards has its own directory structure. By default under
    :code:`/opt/gnuhealth/his-50` . Remember to also copy the contents of your current
    *attach*  directory under this new dir (eg, /opt/gnuhealth/his-50/attach)


**Step 4:** Install the new 5.0 release  as in a new :ref:`techguide-installation-vanilla:vanilla_installation`. This will install GNU Health on a virtual environment.

It will also create the new directory structure (etc, logs, attach, ..)

.. note::
    GNU Health 5.0 onwards has its own directory structure. By default under
    :code:`/opt/gnuhealth/his-50` . Remember to also copy the contents of your current
    *attach*  directory under this new dir (eg, /opt/gnuhealth/his-50/attach)


**Step 5:** (optional) Update the Tryton configuration file :code:`trytond.conf` to fit your needs.


The best way to edit the configuration file is to use the GNU Health user alias :code:`editconf`:


.. code-block:: console


        $ editconf

**Step 6:** Follow the upgrade specific instructions for your release.


.. _techguide-administration-upgrade:upgrade-upgrade_instructions_for_5.0:

Upgrade instructions for 5.0
----------------------------

Make sure you have read this chapter from the beginning and taken all preventive measures before you start.


.. warning::

    Please make sure you have refactor **your local packages** to the new Tryton 7.0 framework.


For upgrading HIS version 4.4 to 5.0 we deliver a script that contains the required steps.

We have made a package from the upgrade utilities relevant to 5.0 version. You can download it from Codeberg:

https://codeberg.org/gnuhealth/his-utils/releases/download/5.0.0/his-utils-main_scripts-upgrade-utils-5.0.tar.gz


.. important::

    The source his-utils-main_scripts-upgrade-utils-5.0.tar.gz is bound to a particular tag / release. For the latest version, check https://codeberg.org/gnuhealth/his-utils/releases


Keep in mind that since GH HIS 5.0 we have a modular approach to installation, so you need to know ahead of time the packages to install for your new version.

Run the migration script:

.. code-block:: console


        $ ./ghupg5.sh -d your_db_name -P admin_passwd

The process will go through different tasks involving Tryton and GNU Health.

.. note::

    Depending on the size of your DB and out-of-sync records, this process can take
    several hours.

