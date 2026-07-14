.. _appendix-opsystem:operating_system-specific_notes:

Operating System-Specific Notes
===============================

.. _appendix-opsystem:operating_system-specific_notes-freebsd:

FreeBSD
-------

.. _appendix-opsystem:operating_system-specific_notes-freebsd-at_operating_system_installation:

At Operating System installation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Choose ZFS filesystem and encryption
* Create the gnuhealth user at installation time
* Select SSHD and NTP services at boot time

.. _appendix-opsystem:operating_system-specific_notes-freebsd-install_requirements:

Install requirements
^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

        # pkg install python
        # pkg install postgresql16-server
        # pkg install wget bash patch rust
        # pkg install cmake gmake libxml2 libxslt jpeg-turbo



.. _appendix-opsystem:operating_system-specific_notes-freebsd-initialize_postgresql:

Initialize PostgreSQL
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

        # /usr/local/etc/rc.d/postgresql initdb
        # sysrc postgresql_enable=yes
        # service postgresql start

.. _appendix-opsystem:operating_system-specific_notes-freebsd-create_python3_links:


.. _appendix-opsystem:operating_system-specific_notes-freebsd-change_/bin/bash_to_/usr/local/bin/bash:


.. _appendix-opsystem:operating_system-specific_notes-freebsd-requirements_for_gtk_client:

Requirements for GTK client
^^^^^^^^^^^^^^^^^^^^^^^^^^^

You have to install some requirements as system packages before installing the client using pip:

.. code-block:: console

        # pkg install gcc py39-gobject3 py39-pip


.. _appendix-opsystem:operating_system-specific_notes-debian:

Debian
------

.. _appendix-opsystem:operating_system-specific_notes-debian-download_and_install_the_operating_system:

Download and install the Operating System
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Download the Debian OS  `image <https://www.debian.org>`_
* Check the partitioning and FS options (we use ext4 filesystem)
* Choose XFCE (optional)
* Enable SSHD server
* Create the user "gnuhealth" when prompted at installation time.

.. _appendix-opsystem:operating_system-specific_notes-debian-install_the_requirements:

Install the requirements
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

        $ sudo apt-get install postgresql patch python3-pip python3-venv wget libreoffice-nogui gettext libpq-dev python3-dev python-is-python3

.. _appendix-opsystem:operating_system-specific_notes-debian-allow_local_pip_installation:


**Next step**: :ref:`techguide-installation-vanilla:vanilla_installation-installing_gnu_health_on_gnu/linux_and_freebsd-creating_the_operating_system_user`

.. _appendix-opsystem:operating_system-specific_notes-debian-requirements_for_gtk_client:

Requirements for GTK client
^^^^^^^^^^^^^^^^^^^^^^^^^^^

You have to install some requirements as system packages before installing the client using pip:

.. code-block:: console

        $ sudo apt install python3-gi python3-gi-cairo python3-goocalendar gir1.2-gtk-3.0 libcairo2-dev libgirepository1.0-dev python3-dev python3-pip gcc


.. _appendix-opsystem:operating_system-specific_notes-void_linux:

Void Linux
----------

* Download Void `<https://voidlinux.org>`_
* Download PostgreSQL and activate the service

.. code-block:: console

        # xbps-install postgresql-16_1 postgresql16-client-16.1_1
        # ln -s /etc/sv/postgresql16/ /var/service

* Check the status of the installation and running server

.. code-block:: console

        # sv status postgresql16


.. _appendix-opsystem:operating_system-specific_notes-void_linux-allow_local_pip_installation:


**Next step**: :ref:`techguide-installation-vanilla:vanilla_installation-installing_gnu_health_on_gnu/linux_and_freebsd-creating_the_operating_system_user`


.. _appendix-opsystem:operating_system-specific_notes-opensuse:

openSUSE
--------

.. note::
        This section provides the instructions for the official and standard (vanilla) installation on openSUSE.
        If you want to use the openSUSE package based installation, please refer to the :ref:`appendix-community:community_pages`

.. _appendix-opsystem:operating_system-specific_notes-opensuse-download_and_install_the_operating_system:

Download and install the Operating System
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Download the openSUSE Leap Network `CD image <https://get.opensuse.org/leap/15.5/>`_
* Check the partitioning and FS options (we use ext4 filesystem)
* Select SERVER (text only) installation
* Enable SSHD server
* Create the user "gnuhealth" when prompted at installation time

.. _appendix-opsystem:operating_system-specific_notes-opensuse-install_the_requirements:

Install the requirements
^^^^^^^^^^^^^^^^^^^^^^^^

We need to use Python3.11

.. code-block:: console

        $ sudo zypper in patch python311

Replace default Python 3.6 with 3.11:

.. code-block:: console

        $ ln -si python3.11 python

Install the rest of dependencies

.. code-block:: console

        $ sudo zypper in patch postgresql15-server postgresql15-server-devel gcc python311-devel libreoffice


Initialize the PostgreSQL environment. The next systemctl start command will generate the initial pg cluster.

.. code-block:: console

        $ sudo systemctl start postgresql
        $ sudo systemctl enable postgresql

.. _appendix-opsystem:operating_system-specific_notes-opensuse-update_locally_pip3:


**Next step**: :ref:`techguide-installation-vanilla:vanilla_installation-installing_gnu_health_on_gnu/linux_and_freebsd-creating_the_operating_system_user`

.. _appendix-opsystem:operating_system-specific_notes-opensuse-requirements_for_gtk_client:

Requirements for GTK client
^^^^^^^^^^^^^^^^^^^^^^^^^^^

You have to install some requirements as system packages before installing the client using pip:

.. code-block:: console

        $ sudo zypper in python3-pip gcc python3-devel cairo-devel gobject-introspection-devel typelib-1_0-Gtk-3_0 python3-gobject-Gdk


.. _appendix-opsystem:operating_system-specific_notes-ubuntu:

Ubuntu
------

* Create the gnuhealth user at installation time
* Enable SSH server

.. _appendix-opsystem:operating_system-specific_notes-ubuntu-update_the_sources:

Update the Sources
^^^^^^^^^^^^^^^^^^

.. code-block:: console

        $ sudo apt-get update

.. _appendix-opsystem:operating_system-specific_notes-ubuntu-install_requirements:

Install requirements
^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

        $ sudo apt-get install python3-pip postgresql libreoffice-nogui wget libpq-dev python3-dev

**Next step**: :ref:`techguide-installation-vanilla:vanilla_installation-installing_gnu_health_on_gnu/linux_and_freebsd-creating_the_operating_system_user`

.. _appendix-opsystem:operating_system-specific_notes-ubuntu-requirements_for_gtk_client:

Requirements for GTK client
^^^^^^^^^^^^^^^^^^^^^^^^^^^

You have to install some requirements as system packages before installing the client using pip:

.. code-block:: console

        $ sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0 libcairo2-dev libgirepository1.0-dev python3-dev python3-pip gcc

