.. _techguide-administration-controlcenter:the_gnu_health_control_center:

The GNU Health Control Center
=============================

The GNU Health Control Center :code:`gnuhealth-control` is the main tool for administrative tasks of the :ref:`GNU Health environment<features:features>`.

Since GNU Health HIS 5.0, all the installation and management of the server is done
through **GNU Health Control**.

The new GNU Health control is a self-contained python application that allows you to:

* Install the GNU Health and Tryton server
* Create new DB instances
* Update dependencies
* Install GNU Health packages
* Start and Stop the GNU Health HIS server
* Refresh the Instances (languages, datafiles...)
* Make backups

In an nutshell, gnuhealth-control ("ghcontrol") will do the daily tasks from a single point
of entry. We recommend using gnuhealth-control to perform the administrative tasks, since it
also generates log files of the different tasks that will be very useful in case of problems.

.. _techguide-administration-controlcenter:the_gnu_health_control_center-running_gnuhealth-control:

Running gnuhealth-control
-------------------------

You can invoke gnuhealth-control typing *ghcontrol*

.. code-block:: console

    $ ghcontrol



.. _techguide-administration-controlcenter:the_gnu_health_control_center-server_installation:

Server Installation
-------------------

With gnuhealth-control, you can do the whole server installation. For more information, please refer to
:ref:`techguide-installation-vanilla:vanilla_installation-installation_with_gnu_health_control`


.. _techguide-administration-controlcenter:the_gnu_health_control_center-starting_and_stopping_gnu_health_server:

Starting and Stopping GNU Health Server
---------------------------------------
The GNU Health Control Center allows you to see the current status of the
server. You can also start and stop the server from the menu.

When you start **ghcontrol**, the server status will show in at the bottom
of the screen. It will show in **green** when the server is running and in
**yellow** when is stopped.

.. thumbnail:: ../../images/ghcontrol_start_stop_server.png
    :title: Refresh "tao" instance example
    :width: 70%
    :align: center

To start / stop the server you just need to press on the related submenu
entry.

.. warning::
    Needless to say, stopping the server will immediately shutdown the
    Tryton server, and all operations will stop. It will also affect to
    all the interfaces that are connected to the server.


.. _techguide-administration-controlcenter:the_gnu_health_control_center-choosing_additional_packages:

Choosing additional packages
----------------------------

Depending on your area of work, your institution will need extra functionality that
is provided in the *50+ GNU Health modules*.

This is a very important step in the GNU Health implementation process, because ideally
we should aim for the minimum amount of packages that deliver the functionality we
need. Installing extra packages increases complexity, so please make sure you put
enough time to study the packages you will install.

.. note::
    You can always install packages at a later time.
    If you are new to GNU Health, we recommend you spend some days / weeks using only
    the core package. Once you feel comfortable, you can dive into the remaining
    functionality options.

Here is the list of current GNUHealth HIS :ref:`features:Features`

Now that you know which packages you'd like to include on your institution, let's move
to the package installation section.


.. thumbnail:: ../../images/ghcontrol_add_health_package_entry.png
    :title: GNU Health Control menu entry for adding a new health package.
    :width: 70%
    :align: center

From the main menu, choose "*2: Add Health package*" entry. The next screen will
show you the list of official GNU Health packages for the current version.

.. note::
    For security and integrity reasons, gnuhealth-control only shows official packages.

The following screen shows an example of adding the "lab" package, that provides the GNU Health Laboratory Information System functionality (**Occhiolino**)

.. thumbnail:: ../../images/ghcontrol_selection_health_package_to_add.png
    :title: Example of selecting the lab package from the list.
    :width: 70%
    :align: center



The **all** special package
There is an special package called "*all*". As the name implies, typing *all* in the
package selection field will install the whole list of GNU Health packages, and their
dependencies. This option is mostly used for training or evaluation purposes, and
rarely in production systems.

.. warning::
    Installing all packages increases complexity and reduces modularity. It is
    usually reserved for training and evaluation purposes.


Installing a package will do download the related Pyhton gnuhealth package and
its dependencies. If you want to activate the package in one or more instances, you
need to **refresh** the instance so you can select it and activate it (next section).

.. note::
    Adding a package installs the relevant gnuhealth packages at operating
    system level. The activation of the package is instance dependant.


.. thumbnail:: ../../images/ghcontrol_health_package_installation_ok.png
    :title: The health package installation process was successful
    :width: 70%
    :align: center


If the everything went well, gnuhealth-control will display the message
**"Package(s) Installation OK"** and you are ready to install more packages
or to move to the next section if you're happy :)



.. _techguide-administration-controlcenter:the_gnu_health_control_center-update_packages:

Update packages
---------------
GNU Health Control can keep the system up-to-date. gnuhealth-control will
all the installed gnuhealth, tryton packages and their dependencies, updating those
that are outdated.

.. thumbnail:: ../../images/ghcontrol_update_packages_dependencies.png
    :title: Update Packages and dependencies entry from the main menu
    :width: 70%
    :align: center

Choose "Update Packages / dependencies" in the main menu. GNUHealth-control will
download and install the required updates.


.. thumbnail:: ../../images/ghcontrol_update_dependencies_process.png
    :title: Update Packages and dependencies entry from the main menu
    :width: 70%
    :align: center


.. _techguide-administration-controlcenter:the_gnu_health_control_center-refresh_instance:

Refresh Instance
----------------
Refreshing the instance means registering the new resources in your GNU Health
database instance. The process traverses all the packages, their models, reports,
translations, etc..

.. thumbnail:: ../../images/ghcontrol_refresh_instance_entry.png
    :title: Refresh instance entry from the main menu
    :width: 70%
    :align: center

To refresh a particular instance from gnuhealth-control, you do so by choosing
**"3: Refresh DB instance"** entry from the main menu.

.. note::
    You need to refresh the instance anytime you install a new package.

.. thumbnail:: ../../images/ghcontrol_refresh_instance_result.png
    :title: Refresh "tao" instance example
    :width: 70%
    :align: center



.. _techguide-administration-controlcenter:the_gnu_health_control_center-backup:

Backup
------
To backup your instance, just select the menu entry "Backup Instance" and enter the
instance (db) name.


.. thumbnail:: ../../images/ghcontrol_backup_instance_example.png
    :title: Instance backup process and result.
    :width: 70%
    :align: center

The database backup will be stored with a timestamp inside the **basedir**/log directory.
In the case of an standard installation, will be **/opt/gnuhealth/his-|version-nodot|/backup**

The logs will be in **/opt/gnuhealth/his-|version-nodot|/log**


.. _techguide-administration-controlcenter:the_gnu_health_control_center-restore:

Restore
-------

The backup made by the GNU Health control center allows you to restore a complete GNU Health instance, including the database and the filesystem. Of course, in order to perform a restore, you need to have a backup.

To restore a database, connect with "gnuhealth" operating system user, and change to the directory where the database backup resides.

**Create a new database**:

.. code-block:: console


  $ createdb your_db_name

**Uncompress the database dump that was generated using GNU Health control**:

.. code-block:: console


  $ gunzip backup_db-name_timestamp.gz


**Restore the DB using PostgreSQL**:

.. code-block:: console


  $ psql your_db_name < backup_db-name_timestamp

