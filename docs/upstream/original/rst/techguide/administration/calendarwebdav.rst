.. _techguide-administration-calendarwebdav:calendar_and_webdav:

Calendar and WebDAV
===================

.. _techguide-administration-calendarwebdav:calendar_and_webdav-introduction:

Introduction
------------
GNU Health provides its own WebDAV and Caldav server. It allows to create and associate calendars to health professionals.
The calendar entries for appointments, hospitalizations and other resources can be accessed via WebDAV clients.


.. _techguide-administration-calendarwebdav:calendar_and_webdav-installation:

Installation
------------
To install the webdav functionality, you need to install the following packages

* :code:`pywebdav3-gnuhealth` : Python3 webDAV library for GNU Health (installed automatically when using the standard installation method)
* :code:`health_webdav3_server` : GNU Health webdav server, for Python3 and GNUHealth support
* :code:`health_caldav` : GNU Health calendar package with webdav3 and caldav support
* :code:`health_calendar` : Main calendar for appointments
* :code:`health_inpatient_calendar` : Hospitalization / bed calendar support

If you have installed GNU Health from openSUSE packages, everything is already installed.

.. _techguide-administration-calendarwebdav:calendar_and_webdav-installation-setting_up_the_webdav_server:

Setting up the WebDAV server
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Check the settings for the host and port of the GNUHealth WebDAV server

.. code-block:: ini


        [webdav]
        listen = *:8080

In this sample from the default configuration file, the WebDAV server will accept connections from any network interface, on port 8080.

You can change the values editing the configuration file, using this command:

.. code-block:: console

        $ editconf

.. _techguide-administration-calendarwebdav:calendar_and_webdav-creating_and_assigning_calendars:

Creating and Assigning Calendars
--------------------------------

In order to access a calendar, we first need to create it, and assign it to a user on our GNU Health Tryton instance.

To create a calendar, Follow the link:

**Calendar → Calendars**


* Define a name to the calendar (use only letters, without punctuation or non-ascii characters).
* Assign the calendar to a user (in this example, we assign the "Cordara" Calendar to the "Administrator" user
* Finally, assign the calendar to the user that will login to GNU Health. In this example, the user associated to the "Cordara" calendar is "Administrator", with username "admin". The credentials (username and password) used in the calendar are the same as for login into the GNU Health HIS. For security reasons, use a SSL enabled connection.

.. _techguide-administration-calendarwebdav:calendar_and_webdav-running_the_server:

Running the server
------------------
To start the webdav server, do the following

#. Check that the GNU Health server is running
#. Change to the webdav server directory

.. code-block:: console


        $ cdmods
        $ cd health_webdav3_server/bin


Execute the server

.. code-block:: console


        $ ./gnuhealth-webdav-server


openSUSE comes with a systemd-service called gnuhealth-webdav. It expects the database name as parameter. If your database is gnuhealth34, you can start the service with

.. code-block:: console


        $ systemctl start gnuhealth-webdav@gnuhealth34


.. _techguide-administration-calendarwebdav:calendar_and_webdav-configuring_the_client:

Configuring the client
----------------------

.. _techguide-administration-calendarwebdav:calendar_and_webdav-configuring_the_client-known_clients:

Known clients
^^^^^^^^^^^^^
GNU Health Calendar system has been known to work on the following clients :

* Mozilla Thunderbird, Lightning
* Cadaver
* Evolution

Set the hostname and port of the GNU Health WebDAV server . The default port is :code:`8080`

The nomenclature for the URL is :

:code:`http://your_server_hostname:your_server_port/database_name/Calendars/Calendar_name`
