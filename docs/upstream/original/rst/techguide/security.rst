.. _techguide-security:security:

Security
========

Security is a multi disciplinary task, involving components from networking, operating system, database and application (Tryton), to human resources, to name a few.

This page will try to give an overview of some basic concepts that will help you to enhance the access control to your system. We will also talk about enabling :wikipedia:`Public-key cryptography` to sign documents and records from different models.

.. warning::
        By no means this introductory page will replace the advice of computer security specialists for your specific installation!

.. _techguide-security:security-general_best_practices:

General Best Practices
----------------------

We will focus on GNU Health specific security measures. Nevertheless we start by giving
some general advisories (which are obviously not complete as this is a huge topic itself):

* Keep your Operaing System up to date by doing regular updates. Upgrade your distribution before support of security updates ends.

* Do not publicly expose any ports of productive systems in your hospital or doctors office.

* Use strong passwords, generate and store them securely. For example use KeePassXC and passwords with >=20 digits and special characters included.

* Protect SSH access: At least use SSH keys, disable password based authentication and change the port.
  Think of 2FA, rate limiting and banning malicious IPs for advanced protection.

* Set up a firewall: Restrict access to only expose the needed ports for the needed hosts or subnets.

* Encrypt your file system (see :ref:`techguide-installation-vanilla:vanilla_installation-installing_gnu_health_on_gnu/linux_and_freebsd-encrypting_the_gnuhealth_database_and_attachment_filesystem`)

* Avoid plain HTTP: Use HTTPS/TLS to encrypt your communication between systems and use digital certificates to ensure integrity.

* Check your logfiles regularly, think of using Logwatch for sending them by email or setting up a dedicated monitoring server.

.. _techguide-security:security-gnu_health_security_advisories:

GNU Health Security Advisories
------------------------------

GNU Health releases Security Advisories (SA) anytime a vulnerability is found. The security advisory format is inspired on FreeBSD.

The GNU Health security advisories are sent to all subscribers in the "health-security" mailing list. See the "Resources" chapter to subscribe.

You can check the current security advisory list in https://ftp.gnu.org/gnu/health/security/security_advisories.html


.. _techguide-security:security-use_nginx_and_uwsgi_instead_of_werkzeug:

Use Nginx and uWSGI instead of Werkzeug
---------------------------------------

Trytond comes with a builtin web server that is only intended for development, not for productive use!

We recommend to use uWSGI as application server and Nginx as web server.
Nginx will handle the requests and it is a state of the art solution in terms of security and performance.
See :ref:`techguide-installation-vanilla:vanilla_installation-using_a_wsgi_server_for_gnu_health_hospital_management_component` how to set it up.

There are more options for production grade application and web servers.
But by using the same we can help each other more easily and test and document less.

.. _techguide-security:security-authentication_in_tryton:

Authentication in Tryton
------------------------

Apart from putting strong passwords yourself you can change Trytons configuration:

* Extend or change the authentication method and restrict sessions lifetimes or login attempts:

  https://docs.tryton.org/7.0/server/topics/configuration.html#session
* Configure the password, e.g. define a minimum password length:

  https://docs.tryton.org/7.0/server/topics/configuration.html#password

.. _techguide-security:security-public-key_cryptography_in_gnu_health:

Public-key Cryptography in GNU Health
-------------------------------------

.. _techguide-security:security-public-key_cryptography_in_gnu_health-gnu_health_cryptographic_module:

GNU Health Cryptographic Module
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The module goal is to achieve the concepts of confidentiality, integrity and non-repudiation in GNU Health.

The :code:`health_crypto` module currently provides the following functionality:

* Document Serialization
* Document hashing (MD)
* Document signing
* Document verification

The module will work on records from models that will need this functionality such as prescription, patient evaluations, surgeries or lab tests.

The Serialization includes the information in a predefined format (JSON) and encoding (UTF8).

There will be a field that will contain the Message digest of the serialization process, and that will check for any changes. If the case of alteration of any fields

The signing process will be upon that Message Digest field, whereas the encryption process will work on row or column level.

Public-key / asymmetric cryptography will be used for signing the documents.


The standard models that are included are Prescription, Birth Certificate and Death Certificate.  Of course, you can apply the functionality to any model that you feel like is necessary. In addition, and based on the community requests, we will incorporate new models in the next versions.

.. _techguide-security:security-public-key_cryptography_in_gnu_health-using_digital_signatures_in_gnu_health:

Using Digital Signatures in GNU Health
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



GNU Health works along with :wikipedia:`GNU Privacy Guard` for **digitally signing and verifying documents**. Please refer to the :ref:`plugins-plugins:crypto_plugin` section for the installation

.. _techguide-security:security-reporting_a_security_vulnerability:

Reporting a security vulnerability
----------------------------------
We take security very seriously, and we appreciate your help on this!

If you believe you have found a vulnerability in GNU Health, please send an email to security@gnuhealth.org
