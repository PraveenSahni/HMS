.. _plugins-plugins:introduction:

Introduction
------------
The GNU Health Plugins are client-side programs that provide extra functionality. They are installed locally.

.. _plugins-plugins:initialize_the_plugin_directory:

Initialize the plugin directory
-------------------------------
The GNU Health plugins are installed in your $HOME directory, under "gnuhealth_plugins".

.. code-block:: console


        $ mkdir $HOME/gnuhealth_plugins

In order to keep the GNU Health plugins compatible with the latest client, you need to create a link to the GNU Health plugins directory

.. code-block:: console
        :substitutions:


        $ ln -si $HOME/gnuhealth_plugins $HOME/.config/gnuhealth/|version|/plugins

.. _plugins-plugins:camera_plugin:

Camera Plugin
-------------
The camera plugin allows to visualize, transfer and store media from a webcam device ( camera, microscope, ... ).

There are many contexts where the camera is useful, some of them :

* Person or patient registration
* Domiciliary units surveys
* Histological studies
* EKG strips
* Telemedicine
* Dx Imaging

The information captured by the device will be transferred and stored in the GNU Health server.

.. _plugins-plugins:camera_plugin-installing_opencv:

Installing OpenCV
^^^^^^^^^^^^^^^^^
The GNU Health camera uses the excellent Open Computer Vision library ("OpenCV"). You need to install the opencv package for your operating system.

Install the Python bindings for OpenCV of your distribution. In Debian & openSUSE the package is :code:`python3-opencv` and in Archlinux :code:`python-opencv`.
Besides you can take it directly from PyPI as :code:`opencv-python`.

In order to check the correct installation of OpenCV import the module CV2 in the python interpreter:

.. code-block:: pycon


        $ python3
        Python 3.10.12 (main, Nov 20 2023, 15:14:05) [GCC 11.4.0] on linux
        Type "help", "copyright", "credits" or "license" for more information.
        >>> import cv2
        >>>


If no errors, the installation is successful!

.. _plugins-plugins:camera_plugin-installing_the_camera_plugin:

Installing the Camera Plugin
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Download and uncompress the latest version of the camera plugin and finally move it into your plugins directory:

.. code-block:: console

        $ wget https://codeberg.org/gnuhealth/client-plugins/releases/download/v4.4.1-camera/gnuhealth_plugin_camera-4.4.1.tar.gz
        $ tar -xzvf gnuhealth_plugin_camera-4.4.1.tar.gz
        $ mv gnuhealth_camera $HOME/gnuhealth_plugins/camera

Afterwards restart the client.

.. _plugins-plugins:camera_plugin-invoking_the_camera_plugin:

Invoking the Camera Plugin
^^^^^^^^^^^^^^^^^^^^^^^^^^
From the client, click on the ``Launch action`` icon, and select ``GNU Health Camera``.

.. _plugins-plugins:camera_plugin-using_the_camera:

Using the Camera
^^^^^^^^^^^^^^^^
"**a**" : attach any media taken from the camera device into the current model.

**[SPACE]** : store the media as a binary field, for instance, as the person / patient picture. To store the media as a picture, press the SPACE bar. Currently GNU Health has the party model person picture predefined.

"**h**" : Show the help menu

"**q**" : Quit the camera

After you transfer the media, you need to refresh the current view **[CONTROL + R]**

.. _plugins-plugins:crypto_plugin:

Crypto plugin
-------------
GNU Health implemented signing documents with the GNU Privacy Guard plugin. It could also be modified in order to encrypt documents.

The Crypto plugin works along with the :ref:`GNU Health Crypto Module <techguide-security:security-public-key_cryptography_in_gnu_health-gnu_health_cryptographic_module>`.

.. warning::
        These packages are installed in the client, NOT in the server

In order to use it, you need the following in your client:

* The **GNU Health crypto plugin** itself. It is shipped with the main tarball when following the Vanilla installation.
  Besides it can be downloaded here:

  https://codeberg.org/gnuhealth/client-plugins/releases
* The **GPG package** (comes with most modern operating systems).
* A **GPG key** which is accessible by the operating system user running the client - if you want to make signatures.
* The **python-gnupg library** (https://pypi.org/project/python-gnupg/).

Note that everything except the GPG key is in place when using the Ansible installation with the default configuration (and one is created if setting ``gpg`` to true).


.. _plugins-plugins:crypto_plugin-installation_of_the_crypto_plugin:

Installation of the Crypto plugin
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The procedure is the same as for the camera:

Place the "crypto" directory containing the plugin under the "gnuhealth_plugins" directory.`

.. code-block:: console
        :substitutions:

        $ wget https://codeberg.org/gnuhealth/client-plugins/releases/download/v|release|/gnuhealth_plugin_crypto-|release|.tar.gz
        $ tar -xvf gnuhealth_plugin_crypto-|release|.tar.gz
        $ mv crypto $HOME/gnuhealth_plugins/


.. _plugins-plugins:screenshot_plugin:

Screenshot plugin
-----------------
GNU Health implemented screenshot plugin. It can save screenshots to a record's attachment or set a screenshot as photo of record when possible.

This plugin may be useful when create report include image, for example, lab test report, user can create screenshots from orthanc browser and save them to lab test result's attachement, images saved will be showed in lab test report.

When the plugin create screenshots, it will delay about 2 seconds.

.. warning::
        These packages are installed in the client, NOT in the server

In order to use it, you need the following in your client:

* The **GNU Health Screenshot plugin** itself. It is shipped with the main tarball when following the Vanilla installation.
  Besides it can be downloaded here:

  https://ftp.gnu.org/gnu/health/plugins/gnuhealth_plugin_screenshot-latest.tar.gz


.. _plugins-plugins:screenshot_plugin-installation_of_the_screenshot_plugin:

Installation of the Screenshot plugin
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The procedure is the same as for the camera:

Place the "screenshot" directory containing the plugin under the "gnuhealth_plugins" directory.

.. code-block:: console

        $ wget https://ftp.gnu.org/gnu/health/plugins/gnuhealth_plugin_screenshot-latest.tar.gz
        $ tar -xvf gnuhealth_plugin_screenshot-latest.tar.gz
        $ mv screenshot $HOME/gnuhealth_plugins/


User need to install a screenshot tool or command supported by this plugin, at the moment the plugin support:

1. flameshot: https://flameshot.org/
2. xfce4-screenshooter
3. scrot

Support other screenshot tools or commands is easy, see :code:`get_screenshot_commands` function of screenshot plugin.
