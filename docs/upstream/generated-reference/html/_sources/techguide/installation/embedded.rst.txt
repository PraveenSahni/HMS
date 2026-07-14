.. _techguide-installation-embedded:gnu_health_embedded:

GNU Health Embedded
===================
The GNU Health Embedded sub-project ("GNU Health in a Box") focuses on the installation and use of GNU Health in single-board devices.

The use of GNU Health in single board devices such as the Raspberry Pi has many advantages (in addition to the low cost) such as the easy deployment, little maintenance and low energy consumption that makes it a candidate for some of the following scenarios :

* Remote areas without Internet,
* Academic Institutions,
* Domiciliary Units,
* Vector Control,
* Nursing,
* ICU,
* Laboratory stations, and
* Personal Health Records.

The device is a full server, that has its own database, allowing storing the information locally, without the need of a network. That said, keep in mind that it is a low-resource device, so its usage must be carefully planned, and it's not suitable for high-demand, heavy-load environments, where a regular server would be needed.

.. _techguide-installation-embedded:gnu_health_embedded-raspberry_pi:

Raspberry Pi
------------

About the image
+++++++++++++++

The latest image provides:

* RaspiOS Desktop
* Debian 13 "trixie"
* GNU Health server HIS 5.0 series server and client
* PostgreSQL 17
* Python 3.13

User and initial password for the operating system:

user: gnuhealth
password: freedom


The image also provides a very basic database called "gnuhealthcore", which has the the core and the socioeconomics packages preinstalled. It also has an institution, a health health professional and a patient. The database dump is stored in the "demodb" of the gnuhealth home directory.

user: admin
password: freedom

You can install additional packages using GNU Health control to fit your needs.


Download and Installation
+++++++++++++++++++++++++

You need a 32GB fast SD card, which will leave you around 20GB free for data.

The latest image can be downloaded from the GNU Health official site:

https://www.gnuhealth.org/downloads/embedded/raspberry/gnuhealth_embedded_his50_raspios_debian_13.img.xz

The SHA156 hash is 99cd799ad5d7d8ef63c7e3f564d40dbc85bec0443fa25620c7f4771d73c75a69


*Verify the downloaded file integrity*

.. code-block:: console

    $ sha256sum gnuhealth_embedded_his50_raspios_debian_13.img.xz


*Uncompress the image*

.. code-block:: console

    $ unxz gnuhealth_embedded_his50_raspios_debian_13.img.xz

*Burn the image to the SD card*

.. warning::

    This operation will destroy all the information at the destination device!!
    Make sure you use the right device and not a single partition!!

.. code-block:: console

    $ sudo dd if=gnuhealth_embedded_his50_raspios_debian_13.img of=name_of_your_sd_device (eg /dev/mmblk0) .


Startup
+++++++

Congratulations! You have now GNU Health in a box! The system is configured to startup at boot time, so you just need to click on the GNU Health client icon.
