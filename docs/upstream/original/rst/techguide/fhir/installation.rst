.. _techguide-fhir-installation:installation:

Installation
============
.. _techguide-fhir-installation:installation-about_fhir_and_rest:

About FHIR and REST
-------------------

**Fast Healthcare Interoperability Resources (FHIR)** is a standard for exchanging healthcare information electronically developed by HL7. For more information about FHIR, please see https://hl7.org/fhir

**Representational State Transfer (REST)** is a software architecture style for scalable web services developed by the W3C Technical Architecture Group (TAG). REST based systems can be accessed over the Hypertext Transfer Protocol (HTTP), the same protocol that is used by Web browsers to request Web pages from and to send data to a Web server. For more information about REST, please see https://en.wikipedia.org/wiki/Representational_state_transfer

.. _techguide-fhir-installation:installation-installation:

Installation
------------

The server requires Flask and a few of its addons. And, of course, a working GNU Health installation.

Setup the environment (as the gnuhealth user):

.. code-block:: console

        $ pip install --user gnuhealth-fhir-server


.. _techguide-fhir-installation:installation-configuration:

Configuration
-------------

The server ships with a simple production config file *server/config.py*. However, it needs to be edited.

.. code-block:: python

        TRYTON_DATABASE = ''    #. GNU Health database
        SERVER_NAME = ''        #. Domain name of the server (e.g., fhir.example.com)
        SECRET_KEY = ''         #. Set this value to a long and random string

You can refer to the latest GNU Health FHIR server at pypi:

* `GNU Health FHIR Server <https://pypi.org/project/gnuhealth-fhir-server/>`_

.. _techguide-fhir-installation:installation-security:

Security
--------

In production, always use TLS. Sensitive medical information must be protected and confidential.

By default, all FHIR endpoints except the Conformance statement require user authentication. The user authentication and access follows Tryton’s model, respecting model and field access rights.

The same credentials used to sign into GNU Health are used to access the FHIR REST server.

.. _techguide-fhir-installation:installation-running_the_server:

Running the Server
------------------

For development, you can just run:

.. code-block:: console

        $ python ./gnuhealth_fhir_server.py

For production environments, you should run it from a WSGI container, such as gunicorn, uWSGI or Tornado. In GNU Health we use
uWSGI and nginx as a reverse proxy in production settings for most of our components (Hosptital Management, Thalamus, FHIR..)

.. code-block:: console

        $ uwsgi server_uwsgi.ini


.. _techguide-fhir-installation:installation-troubleshooting:

Troubleshooting
---------------

.. _techguide-fhir-installation:installation-troubleshooting-cannot_connect_to_database:

Cannot connect to database
^^^^^^^^^^^^^^^^^^^^^^^^^^

Make sure you are running as the *gnuhealth* user.

Flask-Tryton should automatically find and parse the Tryton config file. If it is not found:

.. code-block:: python

        TRYTON_CONFIG = ''      # Set this to the path of the Tryton configuration file (e.g., '/weird/tryton/weird-tryton.conf')

.. _techguide-fhir-installation:installation-troubleshooting-no_database_with_that_name:

No database with that name
^^^^^^^^^^^^^^^^^^^^^^^^^^

This is related to the previous error, and occurs when Flask-Tryton cannot find the Tryton config file. Following the previous procedure should hopefully fix it.
