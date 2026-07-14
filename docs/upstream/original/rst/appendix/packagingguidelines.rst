.. _appendix-packagingguidelines:packaging_guidelines:

Packaging Guidelines
====================
In order to make the GNU Health installation and documentation process valid for the vast number of operating systems available, we need to specify some basic guidelines. These guidelines should be taken into account if you want to create a package for your operating system or distribution.
Please note that the package is not required to install GNU Health. The GNU Health installer, detects most operating systems and installs the system and requirements as explained in the installation guide.

If want to create and/or maintain a package for your operating system, please follow these (partial) general guidelines. Note that these guidelines will change from time to time in order to adapt to the new releases.

* **Operating System user** : The operating system user is "gnuhealth"
* **Installation directory** : Installation directory is the $HOME directory of the operating system
* **RC file** : GNU Health comes with a set of pre-defined environment variables and aliases. These are stored in the $HOME/.gnuhealthrc file. It's important that this file is always loaded at login time. The documentation and control programs heavily make use these variables and aliases.
* **Shell** : The default shell, used by the installation script is BASH
* **GNU Health installer** : This is the main installer and its name is gnuhealth-setup, it is included in the main GNU Health tarball. Invoking this script would probably be the easiest way.
* **Directory Structure** : Please follow the directory structure and links that are set during the standard installation.
* **Tryton configuration file** : GNU Health comes with a basic Tryton server configuration file, tailored for the general use.
* **GNU Health control center** : This program is the base for controlling the GNU Health instance (status, backup, updates, language packs ... ). It resides in the "util" directory.

In addition to these basic guidelines, there are a list of per-requisites as per Operating System that must be included. Please check the installation section for your particular Operating System.

.. _appendix-packagingguidelines:packaging_guidelines-desktop_entry:

Desktop Entry
-------------

The GNU Health client contains the :code:`.desktop` file, called :code:`gnuhealth-client.desktop`. For system-wide installation, it can be installed on :code:`/usr/local/share/applications/gnuhealth-client.desktop` in FreeBSD or under :code:`/usr/share/applications/gnuhealth-client.desktop`

When installing the package locally, the gnuhealth-client desktop file can be installed under :code:`$HOME/.local/applications`.

.. _appendix-packagingguidelines:packaging_guidelines-desktop_entry-icon:

Icon
^^^^

The icon we recommend using for the application menu is the scalable :code:`gnuhealth.svg` file (under :code:`gnuhealth/data/pixmaps/gnuhealth`), that can go on the generic :code:`/usr/local/share/icons/hicolor/scalable/apps/gnuhealth.svg` (FreeBSD) or :code:`/usr/share/icons/hicolor/scalable/apps/gnuhealth.svg` on many GNU/Linux distros.
