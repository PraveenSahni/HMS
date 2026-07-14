
.. _techguide-installation-virtualmachine:virtual_machine_image:

Virtual Machine Image
=====================

If you need a ready-to-run server, you can download the Virtualbox image of the
latest Hospital Management System.

This Virtual Machine (VM) has followed the traditional vanilla installation method on a Debian GNU/Linux operating system.

.. _techguide-installation-virtualmachine:virtual_machine_image-operating_system_users_and_initial_passwords:

Operating system users and initial passwords
--------------------------------------------

- gnuhealth: The admin user for the the HMIS server (passwd: "gnu")
- root: Its password is "gnu"


.. important:: Make sure you change both passwords

The server uses the official ("vanilla") installation method, so all
the links, aliases, logs  and documentation are current.

The HMIS server is enabled by default. It runs automatically at
operating system boot time.

Demo DB: We have also included the demo DB "health50", same as the one
in the community server. The credentials are the same
(admin/gnusolidario)

You can create your own database and customize the server. This is a
full blown server and operating system ready to use.

Disk space: In order to save resources and download times this is a
*very* small image. You need to resize the disk and filesystem if you
are going to use it in production.

If you need a larger or custom image for your health institution, you
can contact us at health@gnusolidario.org .

The image is compressed in gzip format. Make sure you uncompress it
before importing into virtualbox.
You can download the latest image here:

https://www.gnuhealth.org/downloads/images/GNUHealth-50-debian12.vdi.gz

.. _techguide-installation-virtualmachine:virtual_machine_image-virtual_machine_specifications:

Virtual Machine Specifications
------------------------------

::

  MD5 hash: a756ac5afe0b93ae705e933e74cbb1c0 GNUHealth-50-debian12.vdi.gz

  Debian: 12.0 "Bookworm"
  DB: Postgresql 15
  Python: 3.11
  Tryton: 7.0
  Desktop environment : XFCE




